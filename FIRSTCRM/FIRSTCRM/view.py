#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/9/27    22:21
#__author__='Administrator'
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout


#用户认证
def acc_login(request):
    errors={}
    if request.method =="POST":
        _email=request.POST.get('email')
        _password=request.POST.get('password')
        user =authenticate(username=_email,password=_password)#调用用户认证模块
        print('login,user',user)
        if user:
            login(request,user)#记录登陆
            next_url =request.GET.get('next','/')#跳转的页面,默认为首页
            return redirect(next_url)
        else:
            errors['error']='认证失败!'
    return render(request,'login.html',locals())

#注销
def acc_logout(request):
    logout(request)
    return redirect('/accounts/login/')

#主页
def index(requset):
    return render(requset,'index.html',locals())