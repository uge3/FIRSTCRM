from django.contrib import admin
from crm import models

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import render,HttpResponse,redirect
from crm.models import UserProfile

#重写admin
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#重写admin
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    #password = ReadOnlyPasswordHashField()#哈值
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("原始密码不存储,所以没有办法看到"
                    "这个用户的密码,但是你可以改变密码 "
                    "使用 <a href=\"../password/\">修改密码</a>."))#哈值

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

#重写admin
class UserProfileAdmin(UserAdmin):#用户类,继承上一个类 UserAdmin
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin', 'is_active','is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('name','stu_account')}),
        ('Permissions', {'fields': ('is_admin','is_active','roles','user_permissions','groups')}),#后台显示
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('roles','user_permissions','groups')#权限

# Now register the new UserAdmin...
admin.site.register(UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):#定制Djanago admin
    list_display = ('id','qq','source','consultant','content','status','date')#显示字段表头
    list_filter = ('source','consultant','date')
    search_fields = ('qq','name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)

    actions = ['test_actions']#定制功能
    def test_actions(self,request,arg2):#对应的函数
        return

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user','name')



#上课记录 讲师
class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ['from_class','day_num','teacher','has_homework','homework_title','homework_content','outline','date']

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
        return redirect("/admin/crm/studyrecord/?course_record__id__exact=%s"%queryset[0].id)#学习记录

    actions = ['initialize_studyrecords',]
    initialize_studyrecords.short_description = "创建班级本节上课记录"#显示别名


#学员 学习记录
class StudyRecordAdmin(admin.ModelAdmin):
    list_display = ['student','course_record','attendance','score','date']
    list_filter =['course_record','attendance','score','course_record__from_class','student']#排序
    list_editable = ['score','attendance']#可编辑

#角色表
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    # fieldsets = ('user_permissions')#权限
    # filter_horizontal = ('permissions',)#权限


admin.site.register(models.Customer,CustomerAdmin)##客户表
admin.site.register(models.Tag)##标签表
admin.site.register(models.CustomerFollowUp)##跟进记录表
admin.site.register(models.Course)#课程表
admin.site.register(models.Branch)#校区
admin.site.register(models.ClassList)#班级表
admin.site.register(models.CourseRecord,CourseRecordAdmin)##课程上课记录表
admin.site.register(models.StudyRecord,StudyRecordAdmin)##学习记录表
admin.site.register(models.Enrollment)##报名表
admin.site.register(models.Payment)##缴费记录
#admin.site.register(models.UserProfile)##帐号表
admin.site.register(models.Role,RoleAdmin)##角色表
#admin.site.register(models.Role)##角色表
admin.site.register(models.Menu)##菜单表
admin.site.register(models.ContractTemplate)##合同表
