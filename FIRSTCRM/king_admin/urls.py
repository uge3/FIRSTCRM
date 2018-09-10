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
from king_admin import views
urlpatterns = [
    url(r'^login/$', views.acc_login, name="acc_logink"),
    url(r'^logout/$', views.acc_logout, name="acc_logoutk"),
    url(r'^$', views.app_index,),#king_admin 对应添加app的主页
    url(r'^(\w+)/$', views.table_index, name='table_index'),#单个具体app页面
    url(r'^(\w+)/(\w+)/$', views.table_data_list,name='table_list'),#表中记录列表
    url(r'^(\w+)/(\w+)/add/$', views.table_add,name="obj_add"),#添加记录
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_change,name="table_change"),#修改信息
    url(r'^(\w+)/(\w+)/(\d+)/change/password/$', views.password_reset,name="password_reset"),#修改密码
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_delete,name="obj_delete"),#删除页面
]