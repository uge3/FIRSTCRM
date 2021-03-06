import json
import os
import time

from utils.permissions_2 import permission
# from utils.permissions import permission
# Create your views here.
from  django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse

from FIRSTCRM import settings
from crm import models


#学员首页
@login_required
@permission.check_permission#权限装饰器
def index(request):
    user_id=request.user.id
    userinfo=models.UserProfile.objects.get(id=user_id)#帐号对象
    roles_list=userinfo.roles.all()#角色列表
    return  render(request,'student/index.html',locals())

#我的课程首页
@login_required
@permission.check_permission#权限装饰器
def my_course(request):
    return  render(request, 'student/my_course.html', locals())

#学习记录列表
@login_required
@permission.check_permission#权限装饰器
def studyrecords(request,enroll_obj_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_obj_id)
    return render(request,'student/studyrecords.html',locals())

#作业详情
@login_required
@permission.check_permission#权限装饰器
def homework_detail(request,enroll_obj_id,studyrecord_id):
    studyrecord_obj=models.StudyRecord.objects.get(id=studyrecord_id)#取学习记录 对象
    enroll_obj=models.Enrollment.objects.get(id=enroll_obj_id)#取班级对象
    print(request.FILES)
    #               作业根目录    班级ID      上课记录ID               学习记录ID
    homework_path="{base_dir}/{class_id}/{course_record_id}/{studyercord_id}/".format(
        base_dir=settings.HOMEWORK_DATA,
        class_id=studyrecord_obj.student.enrolled_class_id,
        course_record_id=studyrecord_obj.course_record_id,
        studyercord_id=studyrecord_obj.id
    )
    print('----->',studyrecord_obj.student.enrolled_class_id,studyrecord_obj.course_record_id,studyrecord_obj.id)
    if not os.path.isdir(homework_path):#没有目录
        os.makedirs(homework_path,exist_ok=True)#创建目录

    if request.method=="POST":#上传
        print("POST",request.POST)
        for k,v in request.FILES.items():#上传的文件
            with open('%s/%s'%(homework_path,v.name),'wb') as f:#chunk 写入文件
                for chunk in v.chunks():
                    f.write(chunk)


    file_lists=[]#已经上传的文件列表
    for file_name in os.listdir(homework_path):
        f_path='%s/%s'%(homework_path,file_name)#文件路径
        modify_time =time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.stat(f_path).st_mtime))#上传时间
        file_lists.append([file_name,os.stat(f_path).st_size,modify_time])#文件列表

    if request.method=="POST":#
        ret=False
        data=request.POST.get('data')
        if data:#如果有删除动作
            del_f_path="%s/%s"%(homework_path,data)#路径
            print(del_f_path,'=-=-=-=-=-=')
            os.remove(del_f_path)
            ret=True
            return HttpResponse(json.dumps(ret))
        print("POST",request.POST)
        return HttpResponse(json.dumps({"status":0,'mag':"上传完成！",'file_lists':file_lists}))
    return render(request,'student/homework_detail.html',locals())



