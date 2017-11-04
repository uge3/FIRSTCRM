"""FIRSTCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from FIRSTCRM import view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view.index),#进入主页
    # url(r'^registers/$', view.registers),#注册
    # url(r'^register/$', view.register),#注册
    # url(r'^check_code.html$', view.check_code),# 验证码 校对
    url(r'^accounts/login/', view.acc_login),#全局login
    url(r'^account/logout/', view.acc_logout,name='acc_logouta'),#全局logout django logout 默认跳转到accounts/login
    url(r'^modify/(\d+)', view.modify,name='acc_modify'),#全局logout django logout 默认跳转到accounts/login
    url(r'^crm/', include('crm.urls')),#客户库
    url(r'^student/', include('student.urls')),#学员
    url(r'^teacher/', include('teacher.urls')),#讲师
    url(r'^sales/', include('sales.urls')),#销售
    url(r'^financial/', include('financial.urls')),#财务
    url(r'^king_admin/', include('king_admin.urls')),#自定义admin
    url(r'^kingadmin/', include('kingadmin.urls')),#自定义admin

]
