
# Create your views here.
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,Http404
import datetime
import re
from django import conf
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from  king_admin import forms
from django.core.cache import cache
from  django.contrib.auth.decorators import login_required
from king_admin.utils.page import pag_list
from django.contrib.auth import login,logout,authenticate
# Create your views here.
#print("dj conf:",conf.settings)

from king_admin import app_config
from king_admin import base_admin
from king_admin.utils.permissions import permission as king_admin_permission
from django.contrib import messages


#模版函数
def acc_login(request):
    err_msg = {}
    today_str = datetime.date.today().strftime("%Y%m%d")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        _verify_code = request.POST.get('verify_code')
        _verify_code_key  = request.POST.get('verify_code_key')

        ##print("verify_code_key:",_verify_code_key)
        ##print("verify_code:",_verify_code)
        if cache.get(_verify_code_key) == _verify_code:
            #print("code verification pass!")

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                request.session.set_expiry(60*60)
                return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/king_admin/")

            else:
                err_msg["error"] = 'Wrong username or password!'

        else:
            err_msg['error'] = "验证码错误!"

    #return render(request,'login.html',{"filename":random_filename, "today_str":today_str, "error":err_msg})
    return render(request,'king_admin/login.html',{ "error":err_msg})


def acc_logout(request):
    logout(request)
    return HttpResponseRedirect("/king_admin/login/")

#app 下表名
#@permission.check_permission
@login_required(login_url="/king_admin/login/")
#@permission.check_permission#权限装饰器
def app_index(request):
    # for app in conf.settings.INSTALLED_APPS:
    #     print(app)
    print("registered_sites",base_admin.site.registered_sites)
    print("sites",base_admin.site)
    return render(request, 'king_admin/app_index.html', {"site":base_admin.site})#返回所有注册app的对象

#单个app
@login_required(login_url="/king_admin/login/")
#@permission.check_permission#权限装饰器
def table_index(request,app_name):
    bases=base_admin.site.registered_sites[app_name]#取出对应app对象
    return render(request, 'king_admin/table_index.html', {"site":bases,'app_name':app_name})

#条件筛选
def filter_querysets(request,queryset):
    condtions = {}#定义一个字典用来存过滤的条件
    print(request.GET,'-------+++++++++++++-----------')
    for k,v in request.GET.items():
        if k in ("page","_o","_q") :continue#判断标签是否存在 自定义的名称
        if v:
            condtions[k] = v#进行配对字典
    print("condtions:",condtions)

    query_res = queryset.filter(**condtions)#调用过滤
    return query_res,condtions

#排序
def get_orderby(request,queryset):
    order_by_key = request.GET.get("_o")
    #order_by_key1=order_by_key.strip()
    if order_by_key: #has sort condtion
        query_res = queryset.order_by(order_by_key.strip())
    else:
        query_res = queryset.order_by("-id")
    return query_res

#关键字
def get_queryset_search_result(request,queryset,admin_obj):
    search_key = request.GET.get("_q", "")#取定义名,默认为空
    q_obj = Q()#多条件搜索
    q_obj.connector = "OR" # or/或 条件
    for column in admin_obj.search_fields:
        q_obj.children.append(("%s__contains" % column, search_key))#运态添加多个条件
    res = queryset.filter(q_obj)#对数据库进行条件搜索
    return res#返回结果

#详细列表
@login_required(login_url="/king_admin/login/")
#@permission.check_permission
@king_admin_permission.check_permission#kingadmin权限装饰器
def table_data_list(request,app_name,model_name,embed=False):
    #print(request,app_name,model_name)
    #admin_obj = base_admin.site.registered_sites[app_name][model_name]#获取到表名的数据
    errors = []
    if app_name in base_admin.site.registered_sites:
        ##print(enabled_admins[url])
        if model_name in base_admin.site.registered_sites[app_name]:
            admin_obj = base_admin.site.registered_sites[app_name][model_name]
    #print(admin_obj)
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
            return_data ={
                "admin_obj":admin_obj,
                 'app_name':app_name,
                "model_name":model_name,
                'objs':objs,
                'page':page,
                 'errors':errors,
                 'request':request
                          }
            if embed:
                return return_data
            else:
                return render(request, "king_admin/table_data_list.html", locals())#locals 返回一个包含当前范围的局部变量字典。
    else:
        raise Http404("url %s/%s not found" % (app_name,model_name) )

#修改内容
#@permission.check_permission
@login_required(login_url="/king_admin/login/")
def table_change(request,app_name,model_name,obj_id):
    admin_obj = base_admin.site.registered_sites[app_name][model_name]#表对象
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj)#modelform 生成表单 加验证
    obj = admin_obj.model.objects.get(id=obj_id)#根据ID获取数据记录
    if request.method == "GET":#如果是 GET 表示 是添加记录
        obj_form = model_form(instance=obj)#数据传入表单
    elif request.method == "POST":#如果是 POST 表示 是修改后的数据
        obj_form = model_form(instance=obj,data=request.POST)#更新数据
        if obj_form.is_valid():
            obj_form.save()
            messages.info(request, '保存成功!', extra_tags='', fail_silently=False)

    return render(request, "king_admin/table_change.html", locals())

#添加
#@permission.check_permission
@login_required(login_url="/king_admin/login/")
def table_add(request,app_name,model_name):
    admin_obj = base_admin.site.registered_sites[app_name][model_name]#表对象
    admin_obj.is_add_form=True#表示为新增表单
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj)#生成 表单
    if request.method == "GET":
        print('get--->add', model_form)
        obj_form = model_form()#跳转过来的为空

    elif request.method == "POST":
        obj_form = model_form(data=request.POST)#添加数据
        if obj_form.is_valid():
            try:
                obj_form.save()#表单验证通过保存
            except Exception as e:
                return redirect("/king_admin/%s/%s/" % (app_name,model_name))#转到之前的页面
        if not obj_form.errors:
            return  redirect("/king_admin/%s/%s/" % (app_name,model_name))#转到之前的页面

    return render(request, "king_admin/table_add.html", locals())#locals 返回一个包含当前范围的局部变量字典。


#删除
#@permission.check_permission
@login_required(login_url="/king_admin/login/")
def table_delete(request,app_name,model_name,obj_id):

    admin_obj = base_admin.site.registered_sites[app_name][model_name]#表类
    # model_form = forms.CreateModelForm(request,admin_obj=admin_obj)#生成 表单
    obj=admin_obj.model.objects.get(id=obj_id)#类的对象
    app_name=app_name
    if admin_obj.readonly_table:
        errors={'锁定的表单':'该表单:<%s>,已经锁定,不能删除当前记录!'%model_name}
    else:
        errors={}
    if request.method=='POST':
        if  not admin_obj.readonly_table:
            obj.delete()#删除
            return redirect("/king_admin/%s/%s/%s/" % (app_name,model_name,obj_id))#转到列表页面
    return render(request, "king_admin/table_del.html", locals())#locals 返回一个包含当前范围的局部变量字典。


#密码修改
#@permission.check_permission
@login_required(login_url="/king_admin/login/")
def password_reset(request,app_name,model_name,obj_id):
    '''密码修改'''
    admin_obj = base_admin.site.registered_sites[app_name][model_name]#表类
    model_form = forms.CreateModelForm(request,admin_obj=admin_obj)#modelform 生成表单 加验证
    obj=admin_obj.model.objects.get(id=obj_id)#类表的对象
    errors={}#错误提示
    if request.method=='POST':
        _password1=request.POST.get('password1')
        _password2=request.POST.get('password2')
        if _password1==_password2:
            if len(_password1)>8:
                obj.set_password(_password1)
                obj.save()
                return redirect(request.path.rstrip('password/'))
            else:
                errors['password_too_short']='must not less than 8 letters'
        else:
            errors['invalid_password']='passwords are not the same'#密码不一致

    return render(request, "king_admin/password_reset.html", locals())#locals 返回一个包含当前范围的局部变量字典。