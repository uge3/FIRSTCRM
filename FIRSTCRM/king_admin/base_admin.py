

from django.shortcuts import render,redirect
from django.contrib.admin import ModelAdmin, actions

#异常处理类
class AdminRegisterException(Exception):#异常处理
    def __init__(self,msg):
        self.message = msg


class BaseAdmin(object):
    list_display = ()#显示列名
    list_filter = ()#条件搜索
    search_fields = ()#关键字搜索
    list_editable = ()#编辑
    list_per_page = 8#每页显示个数
    readonly_fields = []#不可修改
    filter_horizontal=[]#复选框
    default_actions = ["delete_selected"]
    actions = []#自定功能
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
        return render(request,"king_admin/table_del.html", locals())

class AdminSite(object):
    def __init__(self):
        self.registered_sites = {}#定义一个字典 全局

    def register(self,model,admin_class=None,**options):
        app_name = model._meta.app_label#app名称
        model_name = model._meta.model_name#表名称

        if app_name not in self.registered_sites:#如果字典没有添加过app名
            self.registered_sites[app_name] = {}#进行添加

        if model_name in self.registered_sites[app_name]:#如果表名在app中
            raise AdminRegisterException("app [%s] model [%s] has already registered!" %(app_name,model_name))#异常处理

        if not  admin_class:#如果没有传入 即默认
            #use baseadmin
            admin_class = BaseAdmin#默认格式
        admin_obj = admin_class()#传入定制格式的函数
        admin_obj.model = model#加入要定制的对象

        self.registered_sites[app_name][model_name] = admin_obj#写入字典



site = AdminSite()#调用注册类
