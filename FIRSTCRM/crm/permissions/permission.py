#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/10/9    19:29
#__author__='Administrator'
from django.core.urlresolvers import resolve
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
#from king_admin.permission_list import perm_dic
from crm.permissions.permission_list import perm_dic#权限字典
#权限判断检测
def perm_check(*args,**kwargs):
    request = args[0]
    #resolve_url_obj = resolve(request.path)#解析URL
    #current_url_name = resolve_url_obj.url_name  # 当前url的url_name
    #print('---perm:',request.user,request.user.is_authenticated(),current_url_name)
    #match_flag = False
    url_match = False#url判断
    if request.user.is_authenticated() is False:#如果没有登陆
         return redirect(settings.LOGIN_URL)#跳转到登陆页面

    for key,val in  perm_dic.items():#从权限字典中取相关字段
        url_type=val.get('url_type')#url类型
        per_url=val.get('url')#url别名 字符串
        per_method=val.get('method')# 提交类型
        per_args=val.get('args')# 参数
        print(url_type,'url_type<-----')
        if url_type==1:#如果是静态URL
            if per_url==request.path:#匹配上URL
                url_match=True
        else:  #绝对URL转成动态的URLname
            resolve_url_obj = resolve(request.path)#解析URL
            current_url_name = resolve_url_obj.url_name  # 当前url的url_name
            if current_url_name==per_url:#匹配上URL 别名
                url_match=True
        if url_match:
            if per_method==request.method:#提交类型方法的匹配
                arg_match=True#参数条件默认为成立
                for arg in per_args:#参数判断
                    request_method_func = getattr(request,per_method)#获取相应的对象
                    if not request_method_func.get(arg):#如果取不到对应的参数,即为不满足条件
                        arg_match=False

                if arg_match:#请求 与权限 匹配
                    if request.user.has_perm(key):#判断用户是否该权限
                        return True


    # if all(match_results):
    #     app_name, *per_name = match_key.split('_')
    #     print("--->matched ",match_results,match_key)
    #     print(app_name, *per_name)
    #     perm_obj = '%s.%s' % (app_name,match_key)
    #     print("perm str:",perm_obj)
    #     if request.user.has_perm(perm_obj):
    #         print('当前用户有此权限')
    #         return True
    #     else:
    #         print('当前用户没有该权限')
    #         return False
    #
    # else:
    #     print("未匹配到权限项，当前用户无权限")


#装饰器函数
def check_permission(func):
    def inner(*args,**kwargs):
        print("--->permission",args,kwargs)
        if not perm_check(*args,**kwargs):#如果权限检测不能通过
            request = args[0]
            return render(request, 'page_403.html')#返回到指定的页面
        return func(*args,**kwargs)
    return  inner