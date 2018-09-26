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
    consult_course=models.ForeignKey('Course',verbose_name='咨询课程',related_name='customer',on_delete=models.CASCADE)#外键课程表
    status_choices = ((0,'已报名'),(1,'未报名'),(2,'已退学'))
    status = models.SmallIntegerField(choices=status_choices,default=1)#学员状态
    content=models.TextField()#咨询内容
    consultant=models.ForeignKey('UserProfile',verbose_name='课程顾问',related_name='customer',on_delete=models.CASCADE)#课程顾问
    date=models.DateTimeField(auto_now_add=True)#记录时间
    memo=models.TextField(blank=True,null=True)#备注
    def __str__(self):
        return self.qq
    class Meta:
        verbose_name='客户表'
        verbose_name_plural='客户表'

    def clean_status(self):
        status = self.cleaned_data['status']
        if self.instance.id == None:  # add form
            if status == "signed":
                raise forms.ValidationError(("必须走完报名流程后，此字段才能改名已报名"))
            else:
                return status

        else:
            return status
    def clean_consultant(self):
        consultant = self.cleaned_data['consultant']

        if self.instance.id == None :#add form
            return self._request.user

        elif consultant.id != self.instance.consultant.id:
            raise forms.ValidationError(('Invalid value: %(value)s 课程顾问不允许被修改,shoud be %(old_value)s'),
                                         code='invalid',
                                         params={'value': consultant,'old_value':self.instance.consultant})
        else:
            return consultant

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
    customer=models.ForeignKey('Customer',verbose_name='客户',related_name='customerfollowup',on_delete=models.CASCADE)#外键  跟进的客户
    content=models.TextField(verbose_name='跟进内容')
    consultant=models.ForeignKey('UserProfile',verbose_name='跟进人员',related_name='customerfollowup',on_delete=models.CASCADE)#跟进人员
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
    branch=models.ForeignKey('Branch',verbose_name='校区',related_name='classlist',on_delete=models.CASCADE)#校区
    course=models.ForeignKey('Course',verbose_name='课程',related_name='classlist',on_delete=models.CASCADE)#关联课程
    contract=models.ForeignKey('ContractTemplate',blank=True,null=True,default=1,verbose_name='合同',related_name='classlist',on_delete=models.CASCADE)#合同表
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
    from_class=models.ForeignKey('ClassList',verbose_name='班级',related_name='courserecord',on_delete=models.CASCADE)#班级名
    day_num=models.PositiveSmallIntegerField(verbose_name='第几节(天)')
    teacher=models.ForeignKey("UserProfile",verbose_name='讲师',related_name='courserecord',on_delete=models.CASCADE)#讲师
    has_homework=models.BooleanField(default=True,verbose_name='是否有作业')#是否有作业
    homework_title=models.CharField(max_length=128,blank=True,null=True,verbose_name='作业名称')#作业名称
    homework_content=models.TextField(blank=True,null=True,verbose_name='作业内容')#作业内容
    outline= models.TextField(verbose_name='本节课程大纲')
    date=models.DateField(auto_now_add=True, verbose_name="上课日期")#上课时间
    def __str__(self):
        return '班级:%s第 %s 节'%(self.from_class,self.day_num)#班级,节数


    class Meta:
        unique_together=('from_class','day_num')##班级,节数  联合唯一
        verbose_name='课程上课记录表'
        verbose_name_plural='课程上课记录表'

#学习记录表
class StudyRecord(models.Model):
    '''学习记录表'''
    student=models.ForeignKey("Enrollment",verbose_name='报名学员',related_name='studyrecord',on_delete=models.CASCADE)#外键关联  报名表
    course_record=models.ForeignKey('CourseRecord',verbose_name='上课记录',related_name='studyrecord',on_delete=models.CASCADE)#外键关联 上课记录表
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
    customer=models.ForeignKey('Customer',verbose_name='客户',related_name='enrollment',on_delete=models.CASCADE)#客户  学员
    enrolled_class=models.ForeignKey('ClassList',verbose_name='所报班级',related_name='enrollment',on_delete=models.CASCADE)#班级->课程
    consultant=models.ForeignKey('UserProfile',verbose_name='课程顾问',related_name='enrollment',on_delete=models.CASCADE)#课程顾问
    contract_agreed=models.BooleanField(default=False,verbose_name="学员已同意合同条款")#合同
    contract_approved=models.BooleanField(default=False,verbose_name="合同已审核")#合同
    date=models.DateTimeField(auto_now_add=True)#时间,精确到时分秒
    contract_url=models.TextField(verbose_name='学员合同确认链接',null=True)

    def __str__(self):
        #return '%s %s'%(self.customer,self.enrolled_class)#返回学员所报班级课程
        return '%s  |学员：%s  '%(self.enrolled_class,self.customer.name)#返回学员所报班级课程

    class Meta:
        unique_together=('customer','enrolled_class')#学员,,班级课程
        verbose_name='报名表'
        verbose_name_plural='报名表'


#缴费记录
class Payment(models.Model):
    '''缴费记录'''
    customer=models.ForeignKey('Customer',verbose_name='缴费学员',related_name='payment',on_delete=models.CASCADE)#客户表 学员
    course=models.ForeignKey('Course',verbose_name='所报课程',related_name='payment',on_delete=models.CASCADE)#意向课程
    amount=models.PositiveIntegerField(verbose_name='数额',default=500)#所交金额
    consultant=models.ForeignKey('UserProfile',verbose_name='课程顾问',related_name='payment',on_delete=models.CASCADE)#办理人员 课程顾问
    date=models.DateTimeField("交款日期",auto_now_add=True)#时间

    def __str__(self):
        return '%s %s'%(self.customer,self.amount)#返回学员,金额
    class Meta:
        verbose_name='缴费记录'
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
    # is_staff = models.BooleanField(
    #     verbose_name='staff status',
    #     default=False,
    #     help_text='Designates whether the user can log into this admin site.',
    # )
    roles =models.ManyToManyField("Role",blank=True)#角色关联
    objects = UserProfileManager()#创建
    USERNAME_FIELD ='email'#指定做为用户名字段
    REQUIRED_FIELDS = ['name']#必填字段
    stu_account=models.ForeignKey("Customer",verbose_name='关联学员帐号',blank=True,null=True,help_text='报名成功后创建关联帐户',related_name='userprofile',on_delete=models.CASCADE)

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        # The user is identified by their email address
        #用户确认的电子邮件地址
        return self.email
    def __str__(self):
        return self.name
    def has_perm(self,perm,obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        #"""用户有一个特定的许可吗"""
        #最简单的可能的答案:是的,总是
        return True
    #
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        #'''用户有权限查看应用‘app_label’吗?'''
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        '''“用户的员工吗?”'''
        #最简单的可能的答案:所有管理员都是员工
        return self.is_admin#是不是admin权限
        # return self.is_active

    class Meta:
         verbose_name_plural='帐号表'

         permissions=(
             ('crm_010101_all_table_data_list_GET', '010101_全部查看数据_GET'),
             ('crm_010102_all_table_data_list_POST', '010102_全部查看数据_POST'),
             ('crm_010103_all_table_add_GET', '010103_全部添加数据_GET'),
             ('crm_010104_all_table_add_POST', '010104_全部添加数据_POST'),
             ('crm_010105_all_table_change_GET', '010105_全部修改数据_GET'),
             ('crm_010106_all_table_change_POST', '010106_全部修改数据_POST'),
             ('crm_010107_all_table_delete_GET', '010107_全部删除数据_GET'),
             ('crm_010108_all_table_delete_POST', '010108_全部删除数据_POST'),
             ('crm_010109_all_password_reset_GET', '010109_全部密码重置_GET'),
             ('crm_010110_all_password_reset_POST', '010110_全部密码重置_POST'),

             ('crm_010201_only_view_Branch_GET', '010201_只能查看校区表_GET'),
             ('crm_010202_only_view_Branch_POST', '010202_只能查看校区表_POST'),
             ('crm_010203_only_add_Branch_GET', '010203_只能添加校区表_GET'),
             ('crm_010204_only_add_Branch_POST', '010204_只能添加校区表_POST'),
             ('crm_010205_only_change_Branch_GET', '010205_只能修改校区表_GET'),
             ('crm_010206_only_change_Branch_POST', '010206_只能修改校区表_POST'),
             ('crm_010207_only_delete_Branch_GET', '010207_只能删除校区表_GET'),
             ('crm_010208_only_delete_Branch_POST', '010208_只能删除校区表_POST'),

             ('crm_010301_only_view_ClassList_GET', '010301_只能查看班级表_GET'),
             ('crm_010302_only_view_ClassList_POST', '010302_只能查看班级表_POST'),
             ('crm_010303_only_add_ClassList_GET', '010303_只能添加班级表_GET'),
             ('crm_010304_only_add_ClassList_POST', '010304_只能添加班级表_POST'),
             ('crm_010305_only_change_ClassList_GET', '010305_只能修改班级表_GET'),
             ('crm_010306_only_change_ClassList_POST', '010306_只能修改班级表_POST'),
             ('crm_010307_only_delete_ClassList_GET', '010307_只能删除班级表_GET'),
             ('crm_010308_only_delete_ClassList_POST', '010308_只能删除班级表_POST'),

             ('crm_010401_only_view_Course_GET', '010401_只能查看课程表_GET'),
             ('crm_010402_only_view_Course_POST', '010402_只能查看课程表_POST'),
             ('crm_010403_only_add_Course_GET', '010403_只能添加课程表_GET'),
             ('crm_010404_only_add_Course_POST', '010404_只能添加课程表_POST'),
             ('crm_010405_only_change_Course_GET', '010405_只能修改课程表_GET'),
             ('crm_010406_only_change_Course_POST', '010406_只能修改课程表_POST'),
             ('crm_010407_only_delete_Course_GET', '010407_只能删除课程表_GET'),
             ('crm_010408_only_delete_Course_POST', '010408_只能删除课程表_POST'),

             ('crm_010501_only_view_Customer_GET', '010501_只能查看客户表_GET'),
             ('crm_010502_only_view_Customer_POST', '010502_只能查看客户表_POST'),
             ('crm_010503_only_add_Customer_GET', '010503_只能添加客户表_GET'),
             ('crm_010504_only_add_Customer_POST', '010504_只能添加客户表_POST'),
             ('crm_010505_only_change_Customer_GET', '010505_只能修改客户表_GET'),
             ('crm_010506_only_change_Customer_POST', '010506_只能修改客户表_POST'),
             ('crm_010507_only_delete_Customer_GET', '010507_只能删除客户表_GET'),
             ('crm_010508_only_delete_Customer_POST', '010508_只能删除客户表_POST'),

             ('crm_010601_only_view_CustomerFollowUp_GET', '010601_只能查看跟进表_GET'),
             ('crm_010602_only_view_CustomerFollowUp_POST', '010602_只能查看跟进表_POST'),
             ('crm_010603_only_add_CustomerFollowUp_GET', '010603_只能添加跟进表_GET'),
             ('crm_010604_only_add_CustomerFollowUp_POST', '010604_只能添加跟进表_POST'),
             ('crm_010605_only_change_CustomerFollowUp_GET', '010605_只能修改跟进表_GET'),
             ('crm_010606_only_change_CustomerFollowUp_POST', '010606_只能修改跟进表_POST'),
             ('crm_010607_only_delete_CustomerFollowUp_GET', '010607_只能删除跟进表_GET'),
             ('crm_010608_only_delete_CustomerFollowUp_POST', '010608_只能删除跟进表_POST'),

             ('crm_010701_only_view_Enrollment_GET', '010701_只能查看报名表_GET'),
             ('crm_010702_only_view_Enrollment_POST', '010702_只能查看报名表_POST'),
             ('crm_010703_only_add_Enrollment_GET', '010703_只能添加报名表_GET'),
             ('crm_010704_only_add_Enrollment_POST', '010704_只能添加报名表_POST'),
             ('crm_010705_only_change_Enrollment_GET', '010705_只能修改报名表_GET'),
             ('crm_010706_only_change_Enrollment_POST', '010706_只能修改报名表_POST'),
             ('crm_010707_only_delete_Enrollment_GET', '010707_只能删除报名表_GET'),
             ('crm_010708_only_delete_Enrollment_POST', '010708_只能删除报名表_POST'),

             ('crm_010801_only_view_Payment_GET', '010801_只能查看缴费表_GET'),
             ('crm_010802_only_view_Payment_POST', '010802_只能查看缴费表_POST'),
             ('crm_010803_only_add_Payment_GET', '010803_只能添加缴费表_GET'),
             ('crm_010804_only_add_Payment_POST', '010804_只能添加缴费表_POST'),
             ('crm_010805_only_change_Payment_GET', '010805_只能修改缴费表_GET'),
             ('crm_010806_only_change_Payment_POST', '010806_只能修改缴费表_POST'),
             ('crm_010807_only_delete_Payment_GET', '010807_只能删除缴费表_GET'),
             ('crm_010808_only_delete_Payment_POST', '010808_只能删除缴费表_POST'),

             ('crm_010901_only_view_CourseRecord_GET', '010901_只能查看上课表_GET'),
             ('crm_010902_only_view_CourseRecord_POST', '010902_只能查看上课表_POST'),
             ('crm_010903_only_add_CourseRecord_GET', '010903_只能添加上课表_GET'),
             ('crm_010904_only_add_CourseRecord_POST', '010904_只能添加上课表_POST'),
             ('crm_010905_only_change_CourseRecord_GET', '010905_只能修改上课表_GET'),
             ('crm_010906_only_change_CourseRecord_POST', '010906_只能修改上课表_POST'),
             ('crm_010907_only_delete_CourseRecord_GET', '010907_只能删除上课表_GET'),
             ('crm_010908_only_delete_CourseRecord_POST', '010908_只能删除上课表_POST'),

             ('crm_011001_only_view_StudyRecord_GET', '011001_只能查看学习表_GET'),
             ('crm_011002_only_view_StudyRecord_POST', '011002_只能查看学习表_POST'),
             ('crm_011003_only_add_StudyRecord_GET', '011003_只能添加学习表_GET'),
             ('crm_011004_only_add_StudyRecord_POST', '011004_只能添加学习表_POST'),
             ('crm_011005_only_change_StudyRecord_GET', '011005_只能修改学习表_GET'),
             ('crm_011006_only_change_StudyRecord_POST', '011006_只能修改学习表_POST'),
             ('crm_011007_only_delete_StudyRecord_GET', '011007_只能删除学习表_GET'),
             ('crm_011008_only_delete_StudyRecord_POST', '011008_只能删除学习表_POST'),

             ('crm_011101_only_view_UserProfile_GET', '011101_只能查看账号表_GET'),
             ('crm_011102_only_view_UserProfile_POST', '011102_只能查看账号表_POST'),
             ('crm_011103_only_add_UserProfile_GET', '011103_只能添加账号表_GET'),
             ('crm_011104_only_add_UserProfile_POST', '011104_只能添加账号表_POST'),
             ('crm_011105_only_change_UserProfile_GET', '011105_只能修改账号表_GET'),
             ('crm_011106_only_change_UserProfile_POST', '011106_只能修改账号表_POST'),
             ('crm_011107_only_delete_UserProfile_GET', '011107_只能删除账号表_GET'),
             ('crm_011108_only_delete_UserProfile_POST', '011108_只能删除账号表_POST'),

             ('crm_011201_only_view_Role_GET', '011201_只能查看角色表_GET'),
             ('crm_011202_only_view_Role_POST', '011202_只能查看角色表_POST'),
             ('crm_011203_only_add_Role_GET', '011203_只能添加角色表_GET'),
             ('crm_011204_only_add_Role_POST', '011204_只能添加角色表_POST'),
             ('crm_011205_only_change_Role_GET', '011205_只能修改角色表_GET'),
             ('crm_011206_only_change_Role_POST', '011206_只能修改角色表_POST'),
             ('crm_011207_only_delete_Role_GET', '011207_只能删除角色表_GET'),
             ('crm_011208_only_delete_Role_POST', '011208_只能删除角色表_POST'),

             ('crm_011301_only_view_Tag_GET', '011301_只能查看标签表_GET'),
             ('crm_011302_only_view_Tag_POST', '011302_只能查看标签表_POST'),
             ('crm_011303_only_add_Tag_GET', '011303_只能添加标签表_GET'),
             ('crm_011304_only_add_Tag_POST', '011304_只能添加标签表_POST'),
             ('crm_011305_only_change_Tag_GET', '011305_只能修改标签表_GET'),
             ('crm_011306_only_change_Tag_POST', '011306_只能修改标签表_POST'),
             ('crm_011307_only_delete_Tag_GET', '011307_只能删除标签表_GET'),
             ('crm_011308_only_delete_Tag_POST', '011308_只能删除标签表_POST'),

             ('crm_011401_only_view_FirstLayerMenu_GET', '011401_只能查看一层菜单_GET'),
             ('crm_011402_only_view_FirstLayerMenu_POST', '011402_只能查看一层菜单_POST'),
             ('crm_011403_only_add_FirstLayerMenu_GET', '011403_只能添加一层菜单_GET'),
             ('crm_011404_only_add_FirstLayerMenu_POST', '011404_只能添加一层菜单_POST'),
             ('crm_011405_only_change_FirstLayerMenu_GET', '011405_只能修改一层菜单_GET'),
             ('crm_011406_only_change_FirstLayerMenu_POST', '011406_只能修改一层菜单_POST'),
             ('crm_011407_only_delete_FirstLayerMenu_GET', '011407_只能删除一层菜单_GET'),
             ('crm_011408_only_delete_FirstLayerMenu_POST', '011408_只能删除一层菜单_POST'),

             ('crm_011501_only_view_SubMenu_GET', '011501_只能查看二层菜单_GET'),
             ('crm_011502_only_view_SubMenu_POST', '011502_只能查看二层菜单_POST'),
             ('crm_011503_only_add_SubMenu_GET', '011503_只能添加二层菜单_GET'),
             ('crm_011504_only_add_SubMenu_POST', '011504_只能添加二层菜单_POST'),
             ('crm_011505_only_change_SubMenu_GET', '011505_只能修改二层菜单_GET'),
             ('crm_011506_only_change_SubMenu_POST', '011506_只能修改二层菜单_POST'),
             ('crm_011507_only_delete_SubMenu_GET', '011507_只能删除二层菜单_GET'),
             ('crm_011508_only_delete_SubMenu_POST', '011508_只能删除二层菜单_POST'),

             ('crm_011601_only_view_Groups_GET', '011601_只能查看权限组_GET'),
             ('crm_011602_only_view_Groups_POST', '011602_只能查看权限组_POST'),
             ('crm_011603_only_add_Groups_GET', '011603_只能添加权限组_GET'),
             ('crm_011604_only_add_Groups_POST', '011604_只能添加权限组_POST'),
             ('crm_011605_only_change_Groups_GET', '011605_只能修改权限组_GET'),
             ('crm_011606_only_change_Groups_POST', '011606_只能修改权限组_POST'),
             ('crm_011607_only_delete_Groups_GET', '011607_只能删除权限组_GET'),
             ('crm_011608_only_delete_Groups_POST', '011608_只能删除权限组_POST'),

             ('crm_011701_own_password_reset_GET', '011701_自己密码重置_GET'),
             ('crm_011702_own_password_reset_POST', '011702_自己密码重置_POST'),

             ('crm_020101_all_not_audit_GET', '020101_销售查看全部的客户未审核_GET'),
             ('crm_020103_all_enrollment_GET', '020103_销售给全部的客户报名课程_GET'),
             ('crm_020104_all_enrollment_POST', '020104_销售给全部的客户报名课程_POST'),
             ('crm_020105_all_contract_review_GET', '020105_销售给全部的客户审核合同_GET'),
             ('crm_020116_all_contract_review_POST', '020116_销售给全部的客户审核合同_POST'),

             ('crm_020201_own_enrollment_GET', '020201_销售给自己的客户报名课程_GET'),
             ('crm_020202_own_enrollment_POST', '020202_销售给自己的客户报名课程_POST'),
             ('crm_020203_own_contract_review_GET', '020203_销售给自己的客户审核合同_GET'),
             ('crm_020204_own_contract_review_POST', '020204_销售给自己的客户审核合同_POST'),

             ('crm_030101_all_not_payment_GET', '030101_财务查看全部的客户未缴费_GET'),
             ('crm_030102_all_not_payment_POST', '030102_财务查看全部的客户未缴费_POST'),
             ('crm_030103_all_already_payment_GET', '030103_财务查看全部的客户已缴费_GET'),
             ('crm_030104_all_already_payment_POST', '030104_财务查看全部的客户已缴费_POST'),
             ('crm_030105_all_payment_GET', '030105_财务进行全部的客户缴费_GET'),
             ('crm_030106_all_payment_POST', '030106_财务进行全部的客户缴费_POST'),

             ('crm_040101_own_student_course_GET', '040101_学生查看自己的课程_GET'),
             ('crm_040102_own_student_course_POST', '040102_学生查看自己的课程_POST'),
             ('crm_040103_own_studyrecords_GET', '040103_学生自己的上课记录_GET'),
             ('crm_040104_own_studyrecords_POST', '040104_学生自己的上课记录_POST'),
             ('crm_040105_own_homework_detail_GET', '040105_学生自己的作业详情_GET'),
             ('crm_040106_own_homework_detail_POST', '040106_学生自己的作业详情_POST'),

             ('crm_050101_own_teacher_class_GET', '050101_讲师查看自己的班级_GET'),
             ('crm_050102_own_teacher_class_POST', '050102_讲师查看自己的班级_POST'),
             ('crm_050103_own_teacher_class_detail_GET', '050103_讲师查看自己的课节详情_GET'),
             ('crm_050104_own_teacher_class_detail_POST', '050104_讲师查看自己的课节详情_POST'),
             ('crm_050105_own_teacher_lesson_detail_GET', '050105_讲师查看自己的课节学员_GET'),
             ('crm_050106_own_teacher_lesson_detail_POST', '050106_讲师查看自己的课节学员_POST'),
             ('crm_050107_own_howk_down_GET', '050107_讲师自己的学员作业下载_GET'),
             ('crm_050108_own_howk_down_POST', '050108_讲师自己的学员作业下载_POST'),

             ('crm_060101_own_coursetop_details_GET', '060101_讲师查看自己的班级排名详情_GET'),
             ('crm_060102_own_coursetop_details_POST', '060102_讲师查看自己的班级排名详情_POST'),
             ('crm_060103_own_coursetop_score_GET', '060103_讲师查看自己的班级分数排行_GET'),
             ('crm_060104_own_coursetop_score_POST', '060104_讲师查看自己的班级排分数排行_POST'),
             ('crm_060105_own_coursetop_homework_GET', '060105_讲师查看自己的班级作业排行_GET'),
             ('crm_060106_own_coursetop_homework_POST', '060106_讲师查看自己的班级作业排行_POST'),
             ('crm_060107_own_coursetop_attendance_GET', '060107_讲师查看自己的班级出勤排行_GET'),
             ('crm_060108_own_coursetop_attendance_POST', '060108_讲师查看自己的班级出勤排行_POST'),
                      #king_admin
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

"""权限组"""
from django.contrib.auth.models import Group
class Groups(Group):
    class Meta:
        verbose_name_plural = '权限组'

# ————————74PerfectCRM实现CRM权限和权限组限制URL————————
# ————————75PerfectCRM实现CRM扩展权限————————
from django.contrib.auth.models import Permission
class Permissions(Permission):
    dic_name = models.CharField(_('dic_name'), max_length=255)
    class Meta:
        verbose_name_plural = "扩展权限"
        # ————————75PerfectCRM实现CRM扩展权限————————

# class UserProfile(models.Model):
#     '''帐号表'''
#     user=models.OneToOneField(User)#关联django自带用户表
#     name=models.CharField(max_length=32)
#     roles=models.ManyToManyField('Role',blank=True,null=True)#角色,可多选
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural='帐号表'

#合同模版
class ContractTemplate(models.Model):
    name=models.CharField('合同名称',max_length=64,unique=True)
    template=models.TextField()

    def __str__(self):
        return self.name
    class Meta:

        verbose_name_plural='合同表'

#角色表
class Role(models.Model):
    '''角色表'''
    name=models.CharField(max_length=32,unique=True)#唯一
    menus=models.ManyToManyField('Menu',blank=True,verbose_name='动态菜单')#关联菜单
    menuses = models.ManyToManyField('FirstLayerMenu', verbose_name='一层菜单', blank=True)
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
        verbose_name='动态菜单表'
        verbose_name_plural = "动态菜单表"

#     第一层侧边栏菜单
class FirstLayerMenu(models.Model):
    '''第一层侧边栏菜单'''
    name = models.CharField('菜单名',max_length=64)
    url_type_choices = ((0,'related_name'),(1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64,unique=True)
    order = models.SmallIntegerField(default=0,verbose_name='菜单排序')
    sub_menus = models.ManyToManyField('SubMenu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "第一层菜单"
        verbose_name_plural = "第一层菜单"
#第二层侧边栏菜单
class SubMenu(models.Model):
    '''第二层侧边栏菜单'''

    name = models.CharField('二层菜单名', max_length=64)
    url_type_choices = ((0,'related_name'),(1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64, unique=True)
    order = models.SmallIntegerField(default=0, verbose_name='菜单排序')

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "第二层菜单"
        verbose_name_plural = "第二层菜单"