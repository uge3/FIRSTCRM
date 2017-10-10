#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/9/28    12:40
#__author__='Administrator'
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#分页
def pag_list(page,sorted_queryset,admin_obj):#当前页   排序后数据
    paginator = Paginator(sorted_queryset, admin_obj.list_per_page)#传入排序后数据,制定的每页显示数  # Show 25 contacts per page
    try:
        objs = paginator.page(page)#当前的页面的数据
    except PageNotAnInteger:#如果不是整数
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)#返回第一页面的数据
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)#最后页面的数据
    return objs #返回分页数据