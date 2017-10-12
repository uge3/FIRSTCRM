from django.shortcuts import render,HttpResponse,redirect
from crm import forms,models
from django.db import IntegrityError
import string,random,os#用于生成随机字符串
from django.core.cache import cache
from FIRSTCRM import settings
# Create your views here.
from crm.permissions import permission
#销售首页
@permission.check_permission#权限装饰器
def index(request):
    ''''''
    return render(request, 'sales/sales_index.html')

#客户库
@permission.check_permission#权限装饰器
def customers(request):
    ''''''
    return render(request, 'sales/customers.html')


#报名填写 销售
@permission.check_permission#权限装饰器
def enrollment(request,customer_id):
    ''''''
    msgs={}
    customer_obj=models.Customer.objects.get(id=customer_id)#取到客户信息记录
    #enroll_obj=models.Enrollment.objects.all()#报名表
    enroll_obj_list=customer_obj.enrollment_set.all()#已经报名列表
    #print('customer_obj',customer_obj.enrollment_set.all())
    #print('enroll_obj',enroll_obj)
    if request.method=="POST":
        enroll_form=forms.EnrollmentForm(request.POST)#获取数据
        if enroll_form.is_valid():#表单验证
            msg = '''请将此链接发给客户进行填写：
                    http://127.0.0.1:8000/crm/customer/registration/{enroll_obj_id}/{random_str}/
                '''
            random_str=''.join(random.sample(string.ascii_lowercase+string.digits,8))#生成8位随机字符串
            url_str='''customer/registration/{enroll_obj_id}/{random_str}/'''#报名链接
            try:
                print(enroll_form.cleaned_data,'cleaned')
                enroll_form.cleaned_data['customer']=customer_obj#添加学员对象 记录
                enroll_obj=models.Enrollment.objects.create(**enroll_form.cleaned_data)#创建记录
                sort_url=enroll_obj.id#获取报名表对应的ID
                cache.set(enroll_obj.id,random_str,61000)#加入过期时间
                msgs['msg']=msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)#报名记录对应的id,随机字符串，报名链接
                url_str=url_str.format(enroll_obj_id=enroll_obj.id,random_str=random_str)#报名链接
                print(url_str)
            except IntegrityError as e:
                #取到这条记录
                enroll_obj=models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                         enrolled_class_id=enroll_form.cleaned_data['enrolled_class'].id)
                if enroll_obj.contract_agreed:#学员同意
                    #return redirect('/crm/contract_review/%s/'%enroll_obj.id)#跳转到审核页面
                    return render(request,'sales/contract_prompt.html',locals())#跳转提示页面
                enroll_form.add_error('__all__','记录已经存在，不能重复创建！')
                #random_str=''.join(random.sample(string.ascii_lowercase+string.digits,8))#生成8位随机字符串
                cache.set(enroll_obj.id,random_str,61000)#加入过期时间
                msgs['msg']=msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)#报名记录对应的id
                url_str=url_str.format(enroll_obj_id=enroll_obj.id,random_str=random_str)#报名链接
            print(url_str,'url_str')
            models.Enrollment.objects.filter(id=enroll_obj.id).update(contract_url=url_str)#写入表内 更新
            enroll_obj=models.Enrollment.objects.get(id=enroll_obj.id)#取报名的对象
    else:
        enroll_form=forms.EnrollmentForm()#modelform表单
    return render(request,'sales/enrollment.html',locals())


#学员合同签定
def stu_registration(requset,enroll_id,random_str):
    if cache.get(enroll_id)==random_str:
        print(enroll_id,'customer_id======')
        enroll_obj=models.Enrollment.objects.get(id=enroll_id)#报名记录
        if requset.method=="POST":
            if requset.is_ajax():#ajax上传图片
                print('ajax ')
                enroll_data_dir="%s/%s"%(settings.ENROLLED_DATA,enroll_id)#路径
                if not os.path.exists(enroll_data_dir):#如果不存
                    os.makedirs(enroll_data_dir,exist_ok=True)#创建目录
                for k,file_obj in requset.FILES.items():
                    with open("%s/%s"%(enroll_data_dir,file_obj.name),'wb') as f:
                        for chunk in file_obj.chunks():#写入文件
                            f.write(chunk)
                return HttpResponse('上传完成！')
            customer_form=forms.CustomerForm(requset.POST,instance=enroll_obj.customer)#生成表单

            if customer_form.is_valid():#表单验证通过
                customer_form.save()
                enroll_obj.contract_agreed=True#同意协议
                enroll_obj.save()
                status=1
                return render(requset,'sales/stu_registration.html',locals())
        else:
            if enroll_obj.contract_agreed==True:#如果协议已经签订
                status=1
            else:
                status=0
            customer_form=forms.CustomerForm(instance=enroll_obj.customer)#生成表单

        return render(requset,'sales/stu_registration.html',locals())
    else:
        return HttpResponse('非法链接，请自重！')


#提示页面

def contract_prompt(requset,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    enroll_form=forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form=forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    return render(requset,'sales/contract_prompt.html',locals())




#审核合同
def contract_review(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    #payment_form=forms.PaymentForm()#生成表单
    enroll_form=forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form=forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    return render(request, 'sales/contract_review.html', locals())#

#驳回合同
def enrollment_rejection(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#报名表的对象
    enroll_obj.contract_agreed=False#修改学员已经同意核同
    enroll_obj.save()
    return redirect('/crm/customer/%s/enrollment/'%enroll_obj.customer.id)#跳转到enrollment_rejection

#缴费视图
def payment(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    errors={}
    if request.method=="POST":
        payment_amount=request.POST.get('amount')#缴费金额
        if payment_amount:
            payment_amount=int(payment_amount)
            if payment_amount<500:
                errors['err']='缴费金额不得低于500元！'
            else:
                payment_obj=models.Payment.objects.create(
                    customer=enroll_obj.customer,##客户表 学员
                    course=enroll_obj.enrolled_class.course,#所报课程
                    amount=payment_amount,#缴费金额
                    consultant=enroll_obj.consultant#课程顾问
                )
                enroll_obj.contract_agreed=True#审核通过
                enroll_obj.save()
                enroll_obj.customer.status=0#修改为已报名
                enroll_obj.customer.save()
                return redirect('/king_admin/crm/customer/')#客户表
        else:
            errors['err']='金额不能为空！'
    else:
        payment_form=forms.PaymentForm()#生成表单
    return render(request,'sales/payment.html',locals())


