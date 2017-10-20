
from django.shortcuts import render,HttpResponse
from crm import models
from FIRSTCRM import settings
import os,json,time
from crm.permissions import permission
from  django.contrib.auth.decorators import login_required
# Create your views here.
#销售首页
#@permission.check_permission#权限装饰器
@login_required
@permission.check_permission#权限装饰器
def index(request):
    user_id=request.user.id
    userinfo=models.UserProfile.objects.get(id=user_id)#帐号对象
    roles_list=userinfo.roles.all()#角色列表
    return  render(request,'sales/sales_index.html',locals())