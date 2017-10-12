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
from crm import views
urlpatterns = [
    # url(r'^$', views.index,name='sales_index'),#销售首页
    url(r'^customers/$', views.customers, name="customers"),#客户库
    url(r'^customer/(\d+)/enrollment/$', views.enrollment, name="enrollment"),#报名流程一 下一步
    url(r'^contract_prompt/$', views.contract_prompt, name="contract_prompt"),#报名提示
    url(r'^customer/registration/(\d+)/(\w+)/$', views.stu_registration, name="stu_registration"),#报名流程二 学员签同合
    # url(r'^contract_review/(\d+)/$', views.contract_review, name="contract_review"),#报名流程三  审核
    # url(r'^enrollment_rejection/(\d+)/$', views.enrollment_rejection, name="enrollment_rejection"),#报名流程三 驳回
    # url(r'^payment/(\d+)/$', views.payment, name="payment"),#报名流程四    缴费
    #url(r'^customer/registration/(\d+)-(\d+)-(\d+)/$', views.stu_registration_l, name="stu_registration_l"),#报名流程二 学员签同合
    # url(r'^my_class_list/$', views.my_class_list, name="my_class_list"),#班级
]
