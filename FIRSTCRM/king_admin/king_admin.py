#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/10/3    12:19
#__author__='Administrator'
from crm import models
from django.shortcuts import render,redirect

class BaseAdmin(object):
    list_display = ()#显示列名
    list_filter = ()#条件搜索
    search_fields = ()#关键字搜索
    list_editable = ()#编辑
    list_per_page = 8#每页显示个数
    readonly_fields = []#不可修改
    filter_horizontal=[]#复选框
    default_actions = ["delete_selected"]
    actions = []
    readonly_table=False#默认表单不锁定
    modelform_exclude_fields=[]#排除验证字段
    #默认表单验证 全部 可重写
    def default_form_validation(self,request):
        '''默认表单验证  ==  django form 的clean方法'''
        pass

    # def clean_name(self):#名称验证
    #     print('name,验证',self)
    #     # if not queryset['name']:
    #     #     queryset.add_error('name',"不能为空!")

    #默认删除的函数
    def delete_selected(self,request,queryset):
        print("goint to delete ",queryset)
        app_name=self.model._meta.app_label#app名
        model_name=self.model._meta.model_name#表名
        objs=queryset#类对象
        action=request._admin_action
        print(action,'<-------action')
        if self.readonly_table:
            errors={'锁定的表单':'当前表单已经锁定,不可进行批量删除操作!'}
        else:
            errors={}
        if request.POST.get('delete_confirm')=='yes':
            if not self.readonly_table:
                queryset.delete()
                return redirect('/andemsss/%s/%s/'%(app_name,model_name))
        selected_ids=','.join([str(i.id) for i in queryset])
        print(selected_ids,'<---selected_ids')
        objs=queryset
        return render(request,"kingadmin/table_del.html", locals())

enabled_admins={}
def register(model_class,admin_class=None):
    if  models.UserProfile._meta.app_label not in enabled_admins:
        enabled_admins[models.UserProfile._meta.app_label]={}
    admin_class.model=model_class#添加 关联
    enabled_admins[models.UserProfile._meta.app_label][models.UserProfile._meta.model_name]=admin_class

    return