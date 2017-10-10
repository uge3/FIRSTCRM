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
    url(r'^$', views.app_index, name='app_index'),
    url(r'^(\w+)/$', views.table_index, name='table_index'),
    url(r'^(\w+)/(\w+)/$', views.table_data_list,name='table_list'),
    url(r'^(\w+)/(\w+)/add/$', views.table_add,name="obj_add"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_change,name="table_change"),
    url(r'^(\w+)/(\w+)/(\d+)/change/password/$', views.password_reset,name="password_reset"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_delete,name="obj_delete"),
]