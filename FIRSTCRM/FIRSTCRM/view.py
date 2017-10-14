#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/9/27    22:21
#__author__='Administrator'
import json
from io import BytesIO

from django.contrib.auth import login,authenticate,logout
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect,HttpResponse

from crm import forms,models
from crm.forms.account import RegisterForm
from king_admin.utils.check_code import create_validate_code


def jsonp(request):
    func = request.GET.get('callback')
    content = '%s(100000)' %(func,)
    return HttpResponse(content)

#json 对错误信息对象进行处理
class JsonCustomEncoder(json.JSONEncoder):
    def default(self,field):
        if isinstance(field,ValidationError):#如果是错误信息进行处理
            return {'code':field.code ,'messages':field.messages}
        else:
            return json.JSONEncoder.default(self,field)

#验证码函数
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()#创建内存空间
    img, code = create_validate_code()#调用验证码图片生成函数 返回图片 和 对应的验证码
    img.save(stream, 'PNG')#保存为PNG格式
    request.session['CheckCode'] = code#保存在session中
    return HttpResponse(stream.getvalue())

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



