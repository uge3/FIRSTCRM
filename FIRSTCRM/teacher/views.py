import os

from  django.contrib.auth.decorators import login_required
# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect

from FIRSTCRM import settings
from crm import models
from king_admin import base_admin
from king_admin.utils.page import get_orderby
# from django.core.servers.basehttp import FileWrapper
from king_admin.utils.pagination import Page as Pagination
# from utils.permissions import permission
from utils.permissions_2 import permission


#讲师首页
#@king_admin_permission.check_permission#kingadmin权限装饰器
@login_required
@permission.check_permission#权限装饰器

def index(request):
    user_id=request.user.id
    userinfo=models.UserProfile.objects.get(id=user_id)#帐号对象
    roles_list=userinfo.roles.all()#角色列表
    return  render(request, 'teacher/index_teacher.html',locals())

#讲师所教班级
@login_required
@permission.check_permission#权限装饰器
def teacher_my_classes(request):
    # print(request.user.id,'-------=========')
    user_id=request.user.id
    admin_obj = base_admin.site.registered_sites['crm']['classlist']#取自定每页显示的数量
    print(type(admin_obj),'adminob类型',)
    classlist=models.UserProfile.objects.get(id=user_id).classlist_set.all()#讲师所教班级
    print(classlist,type(classlist),'classlist类型')
    #classlist2=admin_obj.filter(id=user_id).all()
    #queryset,condtions =  filter_querysets(request, classlist)# 调用条件过滤
    #print('condtios',condtions,type(condtions))
    #queryset = get_queryset_search_result(request,queryset,admin_obj)#关键搜索
    #sorted_queryset = get_orderby(request,queryset)#排序

    # print(type(sorted_queryset),sorted_queryset,'sorted_queryset类型')
    # page = request.GET.get('page')#获取当前页面数
    # objs=pag_list(page,sorted_queryset,admin_obj)#调用函数 分页
    # print(type(objs),objs,'objs类型')
    # admin_obj.filter_condtions=condtions#总数量
    # admin_obj.querysets =  objs#数据
    #当前页数 默认为1
    sorted_queryset = get_orderby(request,classlist)#排序
    data_count=len(sorted_queryset)
    print(data_count)
    page = Pagination(request.GET.get('p', 1), data_count)
    #courserecordlist=classes_obj.courserecord_set.all()[page.start:page.end]#上课记录
    courserecordlist=sorted_queryset[page.start:page.end]
    #总页数 传入url
    page_str = page.page_str('/teacher/teacher_my_classes/')
    return render(request,'teacher/teacher_my_classes.html',locals())


#讲师班级修改
@login_required
@permission.check_permission#权限装饰器
def my_classes_change(request,class_id):#讲师班级修改
    return redirect('/king_admin/crm/classlist/%s/change/'%class_id)


#班级学员详情
#@login_required
#@permission.check_permission#权限装饰器

def teacher_class_detail(request,class_id):
    user_id=request.user.id
    classes_obj=models.UserProfile.objects.get(id=user_id).classlist_set.get(id=class_id)#所选的班级
    course_recordlist=classes_obj.courserecord_set.all()#上课记录
    data_count=len(course_recordlist)
    #当前页数 默认为1
    page = Pagination(request.GET.get('p', 1), data_count)
    #courserecordlist=classes_obj.courserecord_set.all()[page.start:page.end]#上课记录
    courserecordlist=course_recordlist[page.start:page.end]
    #总页数 传入url
    page_str = page.page_str('/teacher/teacher_class_detail/%s/'%class_id)
    return render(request, 'teacher/teacher_classes_detail.html', locals())

#本节课的学员
def teacher_class_detail_howk(request,class_id,courserecord_id):
    HOMEWORK_path='/%s/class_id/courserecord_id/'%(settings.HOMEWORK_DATA,)#作业根路径
    classes_obj=models.UserProfile.objects.get(id=request.user.id).classlist_set.get(id=class_id)#所选的班级
    study_record_list=models.CourseRecord.objects.get(id=courserecord_id).studyrecord_set.all()#取本节课所有学员
    data_count=len(study_record_list)
    #当前页数 默认为1
    page = Pagination(request.GET.get('p', 1), data_count)
    studyrecord_list=study_record_list[page.start:page.end]# 切片取当前页的数据
    #总页数 传入url
    page_str = page.page_str('/teacher/teacher_class_detail/%s/%s/'%(class_id,courserecord_id))

    return render(request, 'teacher/teacher_classes_detail_howk.html', locals())

#学员作业下载
def howk_down(request,class_id,courserecord_id,studyrecord_id):
    HOMEWORK_path='%s/%s/%s/%s/'%(settings.HOMEWORK_DATA,class_id,courserecord_id,studyrecord_id)#作业目录

    def file_iterator(file_name, chunk_size=512):#获取文件
        with open(file_name,'rb',) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    if os.path.exists(HOMEWORK_path):#判断目录是否存在
        file_list=os.listdir(HOMEWORK_path)#取目录 下的文件
        print(file_list[0],'file_list<<<<<<<')
        if os.path.exists('%s%s'%(HOMEWORK_path,file_list[0])):#判断文件是否存在
            file_path='%s%s'%(HOMEWORK_path,file_list[0])
            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_list[0])
            return response

    return redirect('/teacher/teacher_class_detail/%s/%s/'%(class_id,courserecord_id))