# Create your views here.
import os

from  django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from FIRSTCRM import settings
from crm import models
from crm.forms import forms
from utils.permissions import permission


#财务首页
@login_required
@permission.check_permission#权限装饰器
def index(request):
    user_id=request.user.id
    userinfo=models.UserProfile.objects.get(id=user_id)#帐号对象
    roles_list=userinfo.roles.all()#角色列表
    return render(request, 'financial/index_financial.html', locals())#


# #待审核
@login_required
@permission.check_permission#权限装饰器
def not_audit(request):
    sign=models.Enrollment.objects.all()#所有的报名表
    print(sign,'sign----->')
    return render(request, 'financial/not_audit.html', locals())#


#审核合同
@login_required
# @permission.check_permission#权限装饰器
def contract_review(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    #payment_form=forms.PaymentForm()#生成表单
    enroll_form= forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form= forms.CustomerForm(instance=enroll_obj.customer)#学员的信息
    enrolled_path='%s/%s/'%(settings.ENROLLED_DATA,enroll_id)#证件上传路径
    if os.path.exists(enrolled_path):#判断目录是否存在
        file_list=os.listdir(enrolled_path)#取目录 下的文件
        imgs_one=file_list[0]
        imgs_two=file_list[1]
    return render(request, 'financial/contract_review.html', locals())#

#驳回合同
@login_required
@permission.check_permission#权限装饰器
def enrollment_rejection(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#报名表的对象
    enroll_obj.contract_agreed=False#修改学员 为不同意
    enroll_obj.save()
    return redirect('/financial/not_audit/')#跳转到财务待审核

#缴费视图
@login_required
@permission.check_permission#权限装饰器
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
                enroll_obj.contract_approved=True#审核通过
                enroll_obj.save()
                enroll_obj.customer.status=0#修改为已报名
                print(enroll_obj.customer.status,'enroll_obj.customer.status')
                enroll_obj.customer.save()
                return redirect('/financial/not_audit/')#跳转到财务待审核
                # return render(request, 'financial/not_audit.html', locals())#
        else:
            errors['err']='金额不能为空！'
    else:
        payment_form= forms.PaymentForm()#生成表单
    return render(request, 'financial/payment.html', locals())