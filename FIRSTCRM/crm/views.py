import json
import os
import random
import string
from io import BytesIO

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, redirect

from FIRSTCRM import settings
from crm import models
from crm.forms import forms
from crm.forms.account import RegisterForm
from king_admin.utils.check_code import create_validate_code
from king_admin.utils.permissions import permission as king_admin_permission
# Create your views here.
from utils.permissions import permission


def jsonp(request):
    func = request.GET.get('callback')
    content = '%s(100000)' %(func,)
    return HttpResponse(content)

#json 对错误信息对象进行处理
class JsonCustomEncoder(json.JSONEncoder):
    def default(self,field):
        if isinstance(field,ValidationError):#如果是错误信息进行处理
            return {'code':field.code ,'messages':field.messages}
        else:
            return json.JSONEncoder.default(self,field)

#验证码函数
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()#创建内存空间
    img, code = create_validate_code()#调用验证码图片生成函数 返回图片 和 对应的验证码
    img.save(stream, 'PNG')#保存为PNG格式
    request.session['CheckCode'] = code#保存在session中
    return HttpResponse(stream.getvalue())

def registers(request):
    user_form= forms.UserProfile()#modelform表单
    if request.method=="POST":
        enroll_form= forms.UserProfile(request.POST)#获取数据
        if enroll_form.is_valid():#表单验证
            pass

    return render(request,'registers.html',locals())

#注册2 ajax 验证
def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method=='GET':
        obj=RegisterForm(request=request, data=request.POST)
        return render(request, 'register.html',{'obj':obj})

    elif request.method=='POST':
        #返回的字符串 字典
        ret={'status':False,'error':None,'data':None}
        #进行验证 调用RegisterForm
        obj=RegisterForm(request=request, data=request.POST)
        if obj.is_valid():
            name = obj.cleaned_data.get('name')#获取用户名
            password = obj.cleaned_data.get('password')
            email= obj.cleaned_data.get('email')
            password=make_password(password,)#密码加密
            #print(username,password,email)
            #数据库添加数据
            models.UserProfile.objects.create(name=name,password=password,email=email,)
            #获取用户数据
            user_info= models.UserProfile.objects. \
                filter(email=email, password=password). \
                values('id', 'name', 'email',).first()
            #nid=user_info.id
            print(user_info,type(user_info),'..........')
            # admin_obj = base_admin.site.registered_sites['crm']['userprofile']#表类
            # user_obj=admin_obj.model.objects.get(id=user_info['id'])#类表的对象
            # user_obj.set_password(password)#加密
            # user_obj.save()
            request.session['user_info'] = user_info
            #print(user_info.id)
            ret['status']=True
            ret['data']=obj.cleaned_data
            # print(obj.cleaned_data)
            # print(ret)
            ret=json.dumps(ret)#转为json格式
            #return HttpResponse(ret)
        else:
            #加入错误信息
            #print(obj.errors)
            ret['error']=obj.errors.as_data()
            #提示为False
            #ret['status']=False
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret,cls=JsonCustomEncoder)
            #print(ret)
            #print(ret)
        return HttpResponse(ret)


#销售首页
@permission.check_permission#权限装饰器
def index(request):
    ''''''
    return render(request, 'sales/sales_index.html')

#客户库
@permission.check_permission#权限装饰器
@king_admin_permission.check_permission#kingadmin权限装饰器
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
        enroll_form= forms.EnrollmentForm(request.POST)#获取数据
        if enroll_form.is_valid():#表单验证
            msg = '''请将此链接发给客户进行填写：
                    http://127.0.0.1:8789/crm/customer/registration/{enroll_obj_id}/{random_str}/
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
        enroll_form= forms.EnrollmentForm()#modelform表单
    return render(request,'sales/enrollment.html',locals())


#学员合同签定
def stu_registration(request,enroll_id,random_str):
    if cache.get(enroll_id)==random_str:
        print(enroll_id,'customer_id======')
        enroll_obj=models.Enrollment.objects.get(id=enroll_id)#报名记录
        enrolled_path='%s/%s/'%(settings.ENROLLED_DATA,enroll_id)#证件上传路径
        img_file_len=0  #文件
        if os.path.exists(enrolled_path):#判断目录是否存在
            img_file_list=os.listdir(enrolled_path)#取目录 下的文件
            img_file_len=len(img_file_list)


        if request.method=="POST":
            ret=False
            data=request.POST.get('data')
            if data:#如果有删除动作
                del_img_path="%s/%s/%s"%(settings.ENROLLED_DATA,enroll_id,data)#路径
                print(del_img_path,'=-=-=-=-=-=')
                os.remove(del_img_path)
                ret=True
                return HttpResponse(json.dumps(ret))

            if request.is_ajax():#ajax上传图片
                print('ajax ')
                enroll_data_dir="%s/%s"%(settings.ENROLLED_DATA,enroll_id)#路径
                if not os.path.exists(enroll_data_dir):#如果不存
                    os.makedirs(enroll_data_dir,exist_ok=True)#创建目录
                for k,file_obj in request.FILES.items():
                    with open("%s/%s"%(enroll_data_dir,file_obj.name),'wb') as f:
                        for chunk in file_obj.chunks():#写入文件
                            f.write(chunk)
                return HttpResponse('上传完成！')
            customer_form= forms.CustomerForm(request.POST, instance=enroll_obj.customer)#生成表单

            if customer_form.is_valid():#表单验证通过
                customer_form.save()
                enroll_obj.contract_agreed=True#同意协议
                enroll_obj.save()
                status=1
                return render(request,'sales/stu_registration.html',locals())
        else:
            if enroll_obj.contract_agreed==True:#如果协议已经签订
                status=1
            else:
                status=0
            customer_form= forms.CustomerForm(instance=enroll_obj.customer)#生成表单

        return render(request,'sales/stu_registration.html',locals())
    else:
        return HttpResponse('非法链接，请自重！')

#提示页面
def contract_prompt(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    enroll_form= forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form= forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    return render(request,'sales/contract_prompt.html',locals())

#审核合同
def contract_review(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    #payment_form=forms.PaymentForm()#生成表单
    enroll_form= forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form= forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    return render(request, 'sales/../templates/financial/contract_review.html', locals())#

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
        payment_form= forms.PaymentForm()#生成表单
    return render(request, 'sales/../templates/financial/payment.html', locals())


