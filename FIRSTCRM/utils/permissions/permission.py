#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/10/9    19:29
#__author__='Administrator'
# from django.core.urlresolvers import resolve
from django.urls import resolve # resolve解析URL
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
import re
#from king_admin.permission_list import perm_dic
from utils.permissions.permission_list import perm_dic#权限字典
#权限判断检测
def perm_check(*args,**kwargs):
    request = args[0]
    print(request,'request.user.is_authenticated()')

    for key,val in  perm_dic.items():#从权限字典中取相关字段
        url_type=val.get('url_type')#url类型
        per_url=val.get('url')#url别名 字符串
        per_method=val.get('method')# 提交类型
        per_args=val.get('args')# 参数
        print(url_type,'url_type<-----',request.path,key)
        url_match = False#url判断 默认为False

        if url_type==1:#如果是静态URL
            if per_url==request.path:#匹配上URL
                url_match=True
        else:
            resolve_url_obj = resolve(request.path)#解析URL #绝对URL转成动态的URLname
            current_url_name = resolve_url_obj.url_name  # 当前url的url_name
            if url_type==2:
                per_re=val.get('relist')#取正则
                res=re.match('^%s'%per_re[0],request.path)#正则匹配
                if res and current_url_name==per_url:#匹配上URL 别名
                    url_match=True
            elif url_type==0:
                if current_url_name==per_url:#匹配上URL 别名
                    url_match=True

        #权限判断 如果URL通过
        if url_match:
            if per_method==request.method:#提交类型方法的匹配
                arg_match=True#参数条件默认为成立
                for arg in per_args:#参数判断
                    request_method_func = getattr(request,per_method)#获取相应的对象
                    if not request_method_func.get(arg):#如果取不到对应的参数,即为不满足条件
                        arg_match=False

                if arg_match:#请求 与权限 匹配
                    print(key,'key--------------判断用户是否该权限',request.user.has_perm)

                    if request.user.has_module_perms(key):#判断用户是否该权限 APP权限
                        return True
                    if request.user.has_perm(key):#判断用户是否该权限 特殊权限
                        print(key,'key--------------判断用户是有该权限－－－－－－－－－－－－－')
                        return True


    else:
        print("未匹配到权限项，当前用户无权限")
        # return False
        # return redirect(settings.LOGIN_URL)#跳转到登陆页面


#装饰器函数
def check_permission(func):

    def inner(*args,**kwargs):
        print("--->permission",args,kwargs)
        request = args[0]
        print(request,'request----------',args,kwargs)
        if request.user.is_superuser == True:
            print('超级管理员')
            return func(*args, **kwargs)  # 直接返回 真
        if not perm_check(*args,**kwargs):#如果权限检测不能通过
            return render(request, 'page_403.html')#返回到指定的页面
        return func(*args,**kwargs)
    return  inner