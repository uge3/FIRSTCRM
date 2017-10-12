from django.shortcuts import render,HttpResponse,redirect
from crm import forms,models
# Create your views here.

from crm.permissions import permission
from  django.contrib.auth.decorators import login_required

#财务首页
@login_required
@permission.check_permission#权限装饰器
def index(request):

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
@permission.check_permission#权限装饰器
def contract_review(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)#取对象
    #payment_form=forms.PaymentForm()#生成表单
    enroll_form=forms.EnrollmentForm(instance=enroll_obj)#报名表对象
    customers_form=forms.CustomerForm(instance=enroll_obj.customer)#学员的信息

    return render(request, 'sales/contract_review.html', locals())#

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
        payment_form=forms.PaymentForm()#生成表单
    return render(request,'sales/payment.html',locals())