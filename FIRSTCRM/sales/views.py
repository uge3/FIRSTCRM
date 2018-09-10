
from  django.contrib.auth.decorators import login_required
from django.shortcuts import render

from crm import models
# Create your views here.
from king_admin import views as king_views
from utils.permissions import permission


#销售首页
#@permission.check_permission#权限装饰器
@login_required
@permission.check_permission#权限装饰器
def index(request):
    user_id=request.user.id
    userinfo=models.UserProfile.objects.get(id=user_id)#帐号对象
    roles_list=userinfo.roles.all()#角色列表
    return  render(request,'sales/sales_index.html',locals())

#客户库
@login_required
def sales_customer(request):
    template_data =  king_views.table_data_list(request,"crm",'customer',embed=True)
    request=template_data['request']

    return render(request,'sales/customers.html',template_data)