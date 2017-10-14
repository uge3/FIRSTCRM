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
from teacher import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^$', views.index,name='teacher_index'),#讲师首页
    url(r'^teacher_my_classes/$', views.teacher_my_classes,name='my_teacher_classes'),#讲师班级
    url(r'^teacher_class_detail/(\d+)/$', views.teacher_class_detail,name='teacher_class_detail'),#讲师班级课节详情
    url(r'^teacher_class_detail/(\d+)/(\d+)/$', views.teacher_class_detail_howk,name='teacher_class_detail_howk'),#讲师班级课节详情
    url(r'^homeworks/(\d+)/(\d+)/(\d+)/$', views.howk_down,name='howk_down'),#作业下载
    url(r'^king_admin/crm/classlist/(\d+)/change/$', views.my_classes_change,name='my_classes_change'),#讲师班级修改

]
urlpatterns = format_suffix_patterns(urlpatterns)