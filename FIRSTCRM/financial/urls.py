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
from financial import views
urlpatterns = [
    url(r'^$', views.index,name='financial_index'),#财务首页
    url(r'^not_audit/$', views.not_audit),#财务未审核

    url(r'^contract_review/(\d+)/$', views.contract_review, name="contract_review"),#报名流程三  审核
    url(r'^enrollment_rejection/(\d+)/$', views.enrollment_rejection, name="enrollment_rejection"),#报名流程三 驳回
    url(r'^payment/(\d+)/$', views.payment, name="payment"),#报名流程四    缴费

]