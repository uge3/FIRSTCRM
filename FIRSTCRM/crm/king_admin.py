

from  crm import models
from king_admin.base_admin import site,BaseAdmin
from django.shortcuts import render,redirect,HttpResponse
from django.forms import ModelForm,ValidationError
#print("king_admin crm",models.Customer)
#客户表
class CustomerAdmin(BaseAdmin):
    list_display = ('id','name','qq','consultant','source','consult_course','status','date','enroll')
    list_filter = ('source','status','consultant','consult_course','date')
    search_fields = ('qq','name','consultant__name')#外键用 双下划线
    list_editable = ('status')
    list_per_page = 4
    readonly_fields = ('qq','consultant','tags','status')
    actions = ["change_status",]
    filter_horizontal = ('tags')
    #readonly_table=True#锁定 表单


    def enroll(self):#显示自定义 字段
        print('enroll',self.instance.id)
        if self.instance.status==0:
            link_name='报名新课程'
        else:
            link_name='报名'
        return '<a href="/crm/customer/%s/enrollment/">点击%s</a>'%(self.instance.id,link_name)
    enroll.display_name='报名链接'

    def default_form_validation(self,obj):
        print('validation:制定的',obj.cleaned_data)
        consult_course=obj.cleaned_data.get('content','')#自制验证字段
        if len(consult_course)<10:
            return ValidationError(#添加错误信息 返回
                                ("该字段%(field)s 咨询内容记录不能少于10个字符"),
                                code='invalid',
                                params={'field':'content',},
                            )

    def change_status(self,request,querysets):
        app_name=self.model._meta.app_label#app名
        model_name=self.model._meta.model_name#表名
        print("changeing status",querysets)
        querysets.update(status=1)
        return redirect('/king_admin/%s/%s/'%(app_name,model_name))

    def clean_name(self,obj,*args,**kwargs):#名称验证 单个

        print('-----------------------------')
        name=obj.cleaned_data['name']
        print('-----------------------------')
        if not name:
            obj.add_error('name','不能为空!')
            return ValidationError(#添加错误信息 返回
                                ("%(field)s:该字段 不能为空"),
                                code='invalid',
                                params={'field':'name',},
                            )

        elif len(name)<2:
            obj.add_error('name','不能小于5个字符!')
            #return ValidationError('',)
            return ValidationError(#添加错误信息 返回
                                ("%(field)s:该字段 不能小于5个字符!"),
                                code='invalid',
                                params={'field':'name',},
                            )
    change_status.short_description = "改变报名状态"

    # def clean_name(self):#名称验证 单个
    #     print('name,验证',self.cleaned_data)
    #     if not self.cleaned_data['name']:
    #         self.add_error('name',"不能为空!")


    # def delete_selected(self,request,queryset):
    #     print("goint to delete ",queryset)
    #     app_name=self.model._meta.app_label#app名
    #     model_name=self.model._meta.model_name#表名
    #     objs=queryset#类对象
    #     action=request._admin_action
    #     print(action,'<-------action')
    #     if request.POST.get('delete_confirm')=='yes':
    #         queryset.delete()
    #         return redirect('/andemsss/%s/%s/'%(app_name,model_name))
    #     selected_ids=','.join([str(i.id) for i in queryset])
    #     print(selected_ids,'<---selected_ids')
    #     objs=queryset
    #     return render(request,"king_admin/table_del.html", locals())

#跟进记录表
class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('id','customer','content','consultant','intention','date')
    list_filter = ('intention','consultant','date')

#上课记录 讲师
class CourseRecordAdmin(BaseAdmin):
    list_display = ['from_class','day_num','teacher','has_homework','homework_title','homework_content','outline','date']
    list_filter = ('from_class','teacher','date')
    def initialize_studyrecords(self,request,queryset):#制定功能
        print()
        if len(queryset)>1:
            return HttpResponse("同时只能选择一个班级！")
        print(queryset[0].from_class.enrollment_set.all())
        new_obj_list=[]#用于批量创建  事务
        for enrll_obj in queryset[0].from_class.enrollment_set.all():#创建学习记录
        #     models.StudyRecord.objects.get_or_create(
        #         student=enrll_obj,#对应学员
        #         course_record=queryset[0],
        #         attendance=0,#签到状态,默认签到,
        #         score=0,#成绩
        #     )

            new_obj_list.append(models.StudyRecord(
                student=enrll_obj,#对应学员
                course_record=queryset[0],
                attendance=0,#签到状态,默认签到,
                score=0,#成绩
            ))
        try:
            models.StudyRecord.objects.bulk_create(new_obj_list)#批量创建
        except Exception as e:
            return HttpResponse('批量创建失败,本节课可能有相应的上课记录')
        return redirect("/king_admin/crm/studyrecord/?course_record=%s"%queryset[0].id)#学习记录

    actions = ['initialize_studyrecords',]
    initialize_studyrecords.short_description = "创建班级本节上课记录"#显示别名


#学员 学习记录
class StudyRecordAdmin(BaseAdmin):
    list_display = ['student','course_record','attendance','score','date']
    list_filter =['course_record','attendance','score']#排序
    list_editable = ['score','attendance']#可编辑

    def attendance(self,request,queryset):
        for stud in queryset:
            models.StudyRecord.objects.filter(id=stud.id).update(attendance=0)
        return redirect("/king_admin/crm/studyrecord/?course_record=%s"%queryset[0].course_record.id)#学习记录
    def late(self,request,queryset):
        for stud in queryset:
            models.StudyRecord.objects.filter(id=stud.id).update(attendance=1)
        return redirect("/king_admin/crm/studyrecord/?course_record=%s"%queryset[0].course_record.id)#学习记录
    def absenteeism(self,request,queryset):
        for stud in queryset:
            models.StudyRecord.objects.filter(id=stud.id).update(attendance=2)
        return redirect("/king_admin/crm/studyrecord/?course_record=%s"%queryset[0].course_record.id)#学习记录
    def leave_early(self,request,queryset):
        #print(queryset,'--=-=-=-=--=-==')
        #new_obj_list=[]#用于批量创建  事务
        for stud in queryset:
            models.StudyRecord.objects.filter(id=stud.id).update(attendance=3)
            # new_obj_list.append(models.StudyRecord(
            #     id=stud.id,#对应学员
            #     attendance=3,#签到状态,默认签到,
            # ))
        #models.StudyRecord.objects.  update(new_obj_list)#批量更新
        return redirect("/king_admin/crm/studyrecord/?course_record=%s"%queryset[0].course_record.id)#学习记录

    actions = ['attendance','late','absenteeism','leave_early']
    attendance.short_description = "已签到"#显示别名
    late.short_description = "迟到"#显示别名
    absenteeism.short_description = "缺勤"#显示别名
    leave_early.short_description = "早退"#显示别名

#课程表
class CourseAdmin(BaseAdmin):
    list_display = ('name','outling','price')

#班级表
class ClassListAdmin(BaseAdmin):
    list_filter = ('branch','course','class_type')
    search_fields=('semester','start_date')
    list_display = ('branch','course','semester','class_type','start_date')

#帐号表
class UserProfileAdmin(BaseAdmin):
    list_display = ('email','name')
    readonly_fields = ('password',)
    filter_horizontal = ('user_permissions','groups')
    modelform_exclude_fields=['last_login',]

#报名表
class EnrollmentAdmin(BaseAdmin):
    list_display = ('customer','enrolled_class','consultant','contract_agreed','contract_approved')
    list_filter =['enrolled_class','consultant']#排序
    # readonly_fields = ['contract_agreed']#不可修改

site.register(models.StudyRecord,StudyRecordAdmin)
site.register(models.CourseRecord,CourseRecordAdmin)
site.register(models.Customer,CustomerAdmin)
site.register(models.ClassList,ClassListAdmin)
site.register(models.Course,CourseAdmin)
site.register(models.UserProfile,UserProfileAdmin)
site.register(models.Enrollment,EnrollmentAdmin)
site.register(models.CustomerFollowUp,CustomerFollowUpAdmin)


