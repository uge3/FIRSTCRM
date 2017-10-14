from django.shortcuts import render,HttpResponse,redirect
from crm import models
from FIRSTCRM import settings
import os,json,time
from crm.permissions import permission
from king_admin.utils.permissions import permission as king_admin_permission
from  django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
import FIRSTCRM.settings
# from django.core.servers.basehttp import FileWrapper
from king_admin.utils.pagination import Page as Pagination

#讲师首页
@king_admin_permission.check_permission#kingadmin权限装饰器
@permission.check_permission#权限装饰器
@login_required
def index(request):
    return  render(request, 'teacher/index_teacher.html')

#讲师所教班级
@login_required
@permission.check_permission#权限装饰器
def teacher_my_classes(request):
    # print(request.user.id,'-------=========')
    user_id=request.user.id
    classlist=models.UserProfile.objects.get(id=user_id).classlist_set.all()#讲师所教班级
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
    courserecordlist=classes_obj.courserecord_set.all()#上课记录
    data_count=len(courserecordlist)
    #当前页数 默认为1
    page = Pagination(request.GET.get('p', 1), data_count)
    #总页数 传入url
    page_str = page.page_str('/teacher/teacher_class_detail/%s/'%class_id)
    return render(request, 'teacher/teacher_classes_detail.html', locals())

#本节课的学员
def teacher_class_detail_howk(request,class_id,courserecord_id):
    HOMEWORK_path='/%s/class_id/courserecord_id/'%(settings.HOMEWORK_DATA,)#作业根路径
    classes_obj=models.UserProfile.objects.get(id=request.user.id).classlist_set.get(id=class_id)#所选的班级
    studyrecord_list=models.CourseRecord.objects.get(id=courserecord_id).studyrecord_set.all()#取本节课所有学员
    data_count=len(studyrecord_list)
    #当前页数 默认为1
    page = Pagination(request.GET.get('p', 1), data_count)
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