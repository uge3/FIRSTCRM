from django.shortcuts import render,HttpResponse,redirect
from crm import models
from FIRSTCRM import settings
import os,json,time
from crm.permissions import permission
from  django.contrib.auth.decorators import login_required

#讲师首页
@permission.check_permission#权限装饰器
@login_required
def index(request):
    return  render(request, 'teacher/index_teacher.html')

#讲师所教班级
@login_required
@permission.check_permission#权限装饰器
def teacher_my_classes(request):
    # print(request.user.id,'-------=========')
    user_id=request.user.id
    classlist=models.UserProfile.objects.get(id=user_id).classlist_set.all()#讲师所教班级
    return render(request,'teacher/teacher_my_classes.html',locals())


#讲师班级修改
@login_required
@permission.check_permission#权限装饰器
def my_classes_change(request,class_id):#讲师班级修改
    return redirect('/king_admin/crm/classlist/%s/change/'%class_id)