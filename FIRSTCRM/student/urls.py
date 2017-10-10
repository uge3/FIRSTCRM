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
from student import views
urlpatterns = [
    url(r'^$', views.index,name='stu_index'),#学员首页
    url(r'^my_classes/$', views.my_classes,name='my_classes'),#班级
    url(r'^studyrecords/(\d+)/$', views.studyrecords,name='studyrecords'),#个人作业列表
    url(r'^homework_detail/(\d+)/(\d+)/$', views.homework_detail,name='homework_detail'),#作业详情


]
