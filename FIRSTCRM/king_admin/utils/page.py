#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/9/28    12:40
#__author__='Administrator'
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
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

def pag_list_2(page,sorted_queryset,numb=5):#当前页   排序后数据
    paginator = Paginator(sorted_queryset, numb)#传入排序后数据,制定的每页显示数  # Show 25 contacts per page
    try:
        objs = paginator.page(page)#当前的页面的数据
    except PageNotAnInteger:#如果不是整数
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)#返回第一页面的数据
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)#最后页面的数据
    return objs #返回分页数据

#条件筛选
def filter_querysets(request,queryset):
    condtions = {}#定义一个字典用来存过滤的条件
    print(request.GET,'-------+++++++++++++-----------')
    for k,v in request.GET.items():
        if k in ("page","_o","_q") :continue#判断标签是否存在 自定义的名称
        if v:
            condtions[k] = v#进行配对字典
    print("condtions:",condtions)

    query_res = queryset.filter(**condtions)#调用过滤
    return query_res,condtions

#排序
def get_orderby(request,queryset):
    order_by_key = request.GET.get("_o")
    #order_by_key1=order_by_key.strip()
    if order_by_key: #has sort condtion
        query_res = queryset.order_by(order_by_key.strip())
    else:
        query_res = queryset.order_by("-id")
    return query_res

#关键字
def get_queryset_search_result(request,queryset,admin_obj):
    search_key = request.GET.get("_q", "")#取定义名,默认为空
    q_obj = Q()#多条件搜索
    q_obj.connector = "OR" # or/或 条件
    for column in admin_obj.search_fields:
        q_obj.children.append(("%s__contains" % column, search_key))#运态添加多个条件
    res = queryset.filter(q_obj)#对数据库进行条件搜索
    return res#返回结果