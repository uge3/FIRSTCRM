
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
    return  render(request,'sales/sales_index.html')