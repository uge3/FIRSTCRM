from django.db import models
from django.contrib.auth.models import User #帐户模块
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Permission
# Create your models here.

#客户表
class Customer(models.Model):
    '''客户表'''
    #           blank   Django admin 创建可以为空 // null 数据库中可以为空
    name=models.CharField(max_length=32,blank=True,null=True,help_text="报名后修改为真实姓名!")
    qq=models.CharField(max_length=64,unique=True)#unigue 唯一值
    qq_name=models.CharField(max_length=64,blank=True,null=True)#qq昵称
    phone=models.CharField(max_length=64,blank=True,null=True,verbose_name='手机号')#手机号
    id_num=models.CharField(max_length=64,blank=True,null=True,verbose_name='身份证号')#身份证号
    email=models.EmailField(max_length=64,blank=True,null=True,verbose_name='邮箱')#email
    sex_choices=((0,'保密'),(1,'男'),(2,'女'))
    sex=models.SmallIntegerField(choices=sex_choices,default=0,verbose_name='性别')
    source_choices =((0,'转介绍'),(1,'QQ群'),(2,'官网'),(3,'百度推广'),(4,'51CTO'),(5,'知乎'),(6,'市场推广'))
    source=models.SmallIntegerField(choices=source_choices)#选择来源
    referral_from=models.CharField(verbose_name='转介绍人QQ',max_length=64,blank=True,null=True)
    tags=models.ManyToManyField('Tag',blank=True,null=True)#标签多对多
    consult_course=models.ForeignKey('Course',verbose_name='咨询课程')#外键课程表
    status_choices = ((0,'已报名'),(1,'未报名'),(2,'已退学'))
    status = models.SmallIntegerField(choices=status_choices,default=1)#学员状态
    content=models.TextField()#咨询内容
    consultant=models.ForeignKey('UserProfile',verbose_name='课程顾问')#课程顾问
    date=models.DateTimeField(auto_now_add=True)#记录时间
    memo=models.TextField(blank=True,null=True)#备注
    def __str__(self):
        return self.qq
    class Meta:
        verbose_name='客户表'
        verbose_name_plural='客户表'

#标签表
class Tag(models.Model):
    name=models.CharField(unique=True,max_length=32)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='标签表'
        verbose_name_plural='标签表'

##跟进记录表
class CustomerFollowUp(models.Model):
    '''跟进记录表'''
    customer=models.ForeignKey('Customer')#外键  跟进的客户
    content=models.TextField(verbose_name='跟进内容')
    consultant=models.ForeignKey('UserProfile')#跟进人员
    date=models.DateTimeField(auto_now_add=True)#时间
    intention_choices=((0,'2周内报名'),(1,'1个月内报名'),(2,'近期无报名计划'),(3,'已经在其它机构报名'),(4,'已报名'),(5,'已拉黑'))
    intention=models.SmallIntegerField(choices=intention_choices)#选择意向
    #date = models.DateTimeField(auto_now_add=True)#记录时间
    def __str__(self):
        #return "<%s:%s>"%(self.customer.qq,self.intention)#返回客户的QQ,意向
        return '%s'%self.customer#返回客户的QQ,意向
    class Meta:
        verbose_name='跟进记录表'
        verbose_name_plural='跟进记录表'

#课程表
class Course(models.Model):
    '''课程表'''
    name=models.CharField(max_length=64,unique=True)
    price=models.PositiveSmallIntegerField()#学费 正数
    period=models.PositiveSmallIntegerField(verbose_name='周期(月)')#周期
    outling=models.TextField()#课程大纲


    def __str__(self):
        return self.name
    class Meta:
        verbose_name='课程表'
        verbose_name_plural='课程表'

#校区
class Branch(models.Model):
    '''校区表'''
    name=models.CharField(max_length=128,unique=True)#校区名
    addr=models.CharField(max_length=128)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='校区表'
        verbose_name_plural='校区表'

#班级表
class ClassList(models.Model):
    '''班级表'''
    branch=models.ForeignKey('Branch')#校区
    course=models.ForeignKey('Course')#关联课程
    contract=models.ForeignKey('ContractTemplate',blank=True,null=True,default=1)#合同表
    class_type_choices=((0,"面授(脱产)"),(1,"面授(周末)"),(2,"网络班"))
    class_type=models.SmallIntegerField(choices=class_type_choices,verbose_name='班级类型')
    semester=models.PositiveSmallIntegerField(verbose_name='学期')
    teacher=models.ManyToManyField('UserProfile')#讲师 关联
    start_date=models.DateField(verbose_name='开班日期')#
    end_date=models.DateField(verbose_name='结业日期',blank=True,null=True)#
    def __str__(self):
        return '%s 校区: 课程：%s %s 第 %s 期'%(self.branch,self.course,self.get_class_type_display(),self.semester)#校区,课程,班级类型,学期
        #return '%s %s %s'%(self.branch,self.course,self.semester)#校区,课程,学期

    class Meta:
        unique_together=('branch','course','semester')#联合唯一 校区,课程,学期
        verbose_name='班级表'
        verbose_name_plural='班级表'

#课程上课记录表
class CourseRecord(models.Model):
    '''课程上课记录表'''
    from_class=models.ForeignKey('ClassList',verbose_name='班级')#班级名
    day_num=models.PositiveSmallIntegerField(verbose_name='第几节(天)')
    teacher=models.ForeignKey("UserProfile",verbose_name='讲师')#讲师
    has_homework=models.BooleanField(default=True,verbose_name='是否有作业')#是否有作业
    homework_title=models.CharField(max_length=128,blank=True,null=True,verbose_name='作业名称')#作业名称
    homework_content=models.TextField(blank=True,null=True,verbose_name='作业内容')#作业内容
    outline= models.TextField(verbose_name='本节课程大纲')
    date=models.DateField(auto_now_add=True)#上课时间
    def __str__(self):
        return '班级:%s第 %s 节'%(self.from_class,self.day_num)#班级,节数


    class Meta:
        unique_together=('from_class','day_num')##班级,节数  联合唯一
        verbose_name='课程上课记录表'
        verbose_name_plural='课程上课记录表'

#学习记录表
class StudyRecord(models.Model):
    '''学习记录表'''
    student=models.ForeignKey("Enrollment")#外键关联  报名表
    course_record=models.ForeignKey('CourseRecord')#外键关联 上课记录表
    attendance_choices=((0,'已签到'),(1,'迟到'),(2,'缺勤'),(3,'早退'))#出勤状态
    attendance=models.SmallIntegerField(choices=attendance_choices,default=0)#出勤状态
    score_choices=((100,'A+'),(90,'A'),(85,'B+'),(80,'B'),(75,'B-'),(70,'C+'),(60,'C'),(40,'C-'),(-50,'D'),(-100,'COPY'),(0,'N/A'))#分数等级
    score=models.SmallIntegerField(choices=score_choices,default=0,blank=True,null=True)#分数等级成绩
    memo=models.TextField(blank=True,null=True)#备注
    date=models.DateField(auto_now_add=True)#日期

    def __str__(self):
        #print(self,'<----student')
        # return '%s %s %s'%(self.student,self.course_record,self.score)#学员,课程,成绩,,
        #return '%s %s %s'%(self.student.consultant.name,self.course_record.from_class,self.score)#学员,课程,成绩,,
        return '%s %s %s'%(self.student.customer.name,self.course_record.from_class,self.score)#学员,课程,成绩,,

    class Meta:
        unique_together=('student','course_record')#
        verbose_name='学习记录表'
        verbose_name_plural='学习记录表'

#报名表
class Enrollment(models.Model):
    '''报名\入学表'''
    customer=models.ForeignKey('Customer',verbose_name='客户')#客户  学员
    enrolled_class=models.ForeignKey('ClassList',verbose_name='所报班级')#班级->课程
    consultant=models.ForeignKey('UserProfile',verbose_name='课程顾问')#课程顾问
    contract_agreed=models.BooleanField(default=False,verbose_name="学员已同意合同条款")#合同
    contract_approved=models.BooleanField(default=False,verbose_name="合同已审核")#合同
    date=models.DateTimeField(auto_now_add=True)#时间,精确到时分秒
    contract_url=models.TextField(verbose_name='学员合同确认链接',null=True)

    def __str__(self):
        #return '%s %s'%(self.customer,self.enrolled_class)#返回学员所报班级课程
        return '学员：%s '%(self.customer.name)#返回学员所报班级课程

    class Meta:
        unique_together=('customer','enrolled_class')#学员,,班级课程
        verbose_name='报名表'
        verbose_name_plural='报名表'


#缴费记录
class Payment(models.Model):
    '''缴费记录'''
    customer=models.ForeignKey('Customer')#客户表 学员
    course=models.ForeignKey('Course',verbose_name='所报课程')#意向课程
    amount=models.PositiveIntegerField(verbose_name='数额',default=500)#所交金额
    consultant=models.ForeignKey('UserProfile')#办理人员 课程顾问
    date=models.DateTimeField(auto_now_add=True)#时间

    def __str__(self):
        return '%s %s'%(self.customer,self.amount)#返回学员,金额
    class Meta:
        verbose_name_plural='缴费记录'


#创建用户和超级用户
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:#没有email 报错
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)#加密
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            name=name
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user

#帐号表
class UserProfile(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True#唯一
    )
    name=models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(_('password'), max_length=128,help_text=mark_safe('''<a href='password/'>修改密码</a>'''))
    is_active = models.BooleanField(default=True)#权限
    is_admin = models.BooleanField(default=False)
    roles =models.ManyToManyField("Role",blank=True)#角色关联
    objects = UserProfileManager()#创建
    USERNAME_FIELD ='email'#指定做为用户名字段
    REQUIRED_FIELDS = ['name']#必填字段
    stu_account=models.ForeignKey("Customer",verbose_name='关联学员帐号',blank=True,null=True,help_text='报名成功后创建关联帐户')

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        # The user is identified by their email address
        #用户确认的电子邮件地址
        return self.email
    def __str__(self):
        return self.name
    # def has_perm(self,perm,obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     #"""用户有一个特定的许可吗"""
    #     #最简单的可能的答案:是的,总是
    #     return True
    # #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     #'''用户有权限查看应用‘app_label’吗?'''
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        '''“用户的员工吗?”'''
        #最简单的可能的答案:所有管理员都是员工
        #return self.is_admin#是不是admin权限
        return self.is_active
    class Meta:
         verbose_name_plural='帐号表'
         permissions=(
                      #kingadmin
                      ('can_access_king_admin',"KINGADMIN 首页"),
                      ('can_table_index',"KINGADMIN_单个app"),
                      ('can_table_list',"KINGADMIN_app中 列表查看"),
                      ('can_access_obj_add',"KINGADMIN_app中 添加"),
                      ('can_access_obj_add_post',"KINGADMIN_app中 添加"),
                      ('can_access_table_change',"KINGADMIN_修改"),
                      ('can_access_table_change_post',"KINGADMIN_修改保存"),
                      ('can_access_obj_delete',"KINGADMIN_删除"),
                      ('can_access_obj_delete_post',"KINGADMIN_删除确认"),
                      ('can_access_password_reset',"KINGADMIN_修改密码"),
                      ('can_access_password_reset_post',"KINGADMIN_修改密码保存"),

                      #销售
                      ('can_sales_index',"销售首页"),
                      ('can_access_customer_list',"查看客户库"),
                      ('can_access_customer_detail',"客户信息详情"),
                      ('can_access_customer_detail_post',"客户信息详情修改"),
                      ('can_access_customer_add',"客户信息添加"),
                      ('can_access_customer_add_post',"客户信息添加保存"),
                      ('can_access_customerfollowup_list',"销售 客户信息跟记录"),
                      ('can_access_customerfollowup_detail',"销售 客户信息跟进详情修改"),
                      ('can_access_customerfollowup_detail_post',"销售 客户信息跟进详情修改保存"),
                      ('can_teacher_classes_customerfollowup_add',"销售 客户信息跟进添加"),
                      ('can_teacher_classes_customerfollowup_add_post',"销售 客户信息跟进添加保存"),


                      ('can_access_enrollment',"报名流程一"),
                      ('can_access_enrollment_post',"报名流程一修改"),
                      #讲师
                      ('can_teacher_index',"讲师首页"),
                      ('can_my_teacher_classes',"讲师查看我的班级"),
                      ('can_teacher_classes_courserecord',"讲师班级上课列表"),
                      ('can_teacher_classes_courserecord_post',"讲师班级上课列表批量创建"),
                      ('can_teacher_classes_courserecord_change',"班级课节"),
                      ('can_teacher_classes_courserecord_change_post',"班级课节保存"),
                      ('can_teacher_classes_courserecord_add',"班级上课添加"),
                      ('can_teacher_classes_courserecord_add_post',"班级上课添加保存"),
                      ('can_teacher_classes_studyrecord',"班级学员上课记录"),
                      ('can_teacher_classes_studyrecord_post',"班级学员上课记录保存"),
                      ('can_teacher_classes_studyrecord_change',"讲师班级学员课节 学习记录"),
                      ('can_teacher_classes_studyrecord_change_post',"讲师班级学员课节 学习记录保存"),
                      #财务
                      ('can_financial_index','财务首页'),
                      ('can_financial_not_audit','财务待审核'),
                      ('can_financial_contract_review','财务审核'),
                      # ('can_financial_contract_review_post','财务审核通过'),
                      ('can_financial_enrollment_rejection','财务驳回'),
                      ('can_financial_payment','财务缴费'),
                      ('can_financial_payment_post','财务缴费确认'),
                      #学员
                      ('can_student_index',"学员首页"),
                      ('can_access_my_course',"学员查看我的课程"),
                      ('can_access_studyrecords',"学员学习记录"),
                      ('can_access_homework_detail',"学员作业详情"),
                      ('can_upload_homework',"学员作业提交"),

                      )




# class UserProfile(models.Model):
#     '''帐号表'''
#     user=models.OneToOneField(User)#关联django自带用户表
#     name=models.CharField(max_length=32)
#     roles=models.ManyToManyField('Role',blank=True,null=True)#角色,可多选
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural='帐号表'

#角色表
class Role(models.Model):
    '''角色表'''
    name=models.CharField(max_length=32,unique=True)#唯一
    menus=models.ManyToManyField('Menu',blank=True)#关联菜单
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='角色表'

#动态菜单表
class Menu(models.Model):
    '''动态菜单表'''
    name=models.CharField(max_length=32)#菜单名
    url_type_choices=((0,'alias'),(1,'absolute_url'))#url类型
    url_type=models.SmallIntegerField(choices=url_type_choices,default=0)#默认选择
    url_name=models.CharField(max_length=64)#url别名
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='菜单表'

#合同模版
class ContractTemplate(models.Model):
    name=models.CharField('合同名称',max_length=64,unique=True)
    template=models.TextField()

    def __str__(self):
        return self.name
    class Meta:

        verbose_name_plural='合同表'