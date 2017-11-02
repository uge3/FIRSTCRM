
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

#客户库
@login_required
def sales_customer(request):
    template_data =  king_views.display_table_list(request,'crm','customer',embed=True)
    if request.method == "POST":#批量操作
        action = request.POST.get("action_select")#要调用的自定制功能函数
        selected_ids = request.POST.get("selected_ids")#前端提交的数据
        print(selected_ids,type(selected_ids),"selected_ids-----")
        #if type(selected_ids)!='str':
        #selected_ids = json.loads(selected_ids)#进行转换数据
        print(selected_ids,type(action),action,"selected_ids==========")
        #print("action:",selected_ids,action)
        if selected_ids :
            #selected_ids = json.loads(selected_ids)#进行转换数据
            selected_objs = admin_obj.model.objects.filter(id__in=selected_ids.split(','))#返回之前所选中的条件
        else:
            raise KeyError('No object selected')

        if hasattr(admin_obj,action):
            action_func = getattr(admin_obj,action)#如果admin_obj 对象中有属性action 则打印self.action的值，否则打印'not find'
            request._admin_action=action#添加action内容
            print(request._admin_action,action,'<--------')
        return action_func(request,selected_objs)


    obj_list  =  admin_obj.model.objects.all()#获取传过来的所有对象
    queryset,condtions =  filter_querysets(request, obj_list)# 调用条件过滤
    #after search
    queryset = get_queryset_search_result(request,queryset,admin_obj)#关键搜索
    print("---->",queryset)

    sorted_queryset = get_orderby(request,queryset)#排序

    page = request.GET.get('page')#获取当前页面数
    objs=pag_list(page,sorted_queryset,admin_obj)#调用函数 分页

    admin_obj.querysets =  objs
    admin_obj.filter_condtions = condtions

    return render(request,'sales/customers.html',locals())