# FIRSTCRM

```
学员管理开发需求：
1.分讲师\学员\课程顾问角色,
2.学员可以属于多个班级,学员成绩按课程分别统计
3.每个班级至少包含一个或多个讲师
4.一个学员要有状态转化的过程 ,比如未报名前,报名后,毕业老学员
5.客户要有咨询纪录, 后续的定期跟踪纪录也要保存
6.每个学员的所有上课出勤情况\学习成绩都要保存
7.学校可以有分校区,默认每个校区的员工只能查看和管理自己校区的学员
8.客户咨询要区分来源
9.加入权限管理，不同用户有不同的权限

```
 实现功能:

1. 讲师\销售(课程顾问)\财务\学员
2. 报名流程:  销售生成报名表, 学员填写相关信息上传证件, 财务人员审核,审核通过,销售进行学员帐号关联
3. 学员可以报名多个班级,学员成绩按课程分别统计
4. 讲师可以教多个班级,每个班级至少包含一个或多个讲师
5. 学员状态,未报名,已报名
6. 销售有咨询纪录,后续的定期跟踪纪录有保存
7. 客户咨询区分来源
8. 学校分校区,默认每个校区的员工只能查看和管理自己校区的学员
9. 每个学员的所有上课出勤情况\学习成绩都保存
10. 加入权限管理，不同用户有不同的权限


程序结构:

```

 FIRSTCRM/#主目录
 |- - -FIRSTCRM/# 主程序目录
 |       |- - -__init__.py
 |       |- - -settings#配置文件
 |       |- - -urls.py#主路由
 |       |- - -view.py/##视图函数
 |       |- - -wsgi.py#WSIG规范文件
 |
 |
 |- - -cache/#缓存目录
 |
 |- - -crm/#CRM程序目录
 |       |- - -forms/#表单验证函数目录
 |       |     |- - -__init__.py
 |       |     |- - -account.py #登陆相关表单验证函数
 |       |     |- - -base.py #登陆基础函数
 |       |     |- - -forms.py #modelsform表单验证函数
 |       |- - -migrations/#数据库操作日志
 |       |     |- - -__init__.py
 |       |- - -permissions/#权限控制组件
 |       |     |- - -__init__.py
 |       |     |- - -permission.py#权限控制函数
 |       |     |- - -permission_list.py#权限控制条件
 |       |     
 |       |
 |       |- - -templatetags/#注册为模块 load
 |       |     |- - -crm_tags.py#合同格式
 |       |- - -__init__.py
 |       |- - -admin.py
 |       |- - -apps.py
 |       |- - -kingadmin.py#自定义admin注册
 |       |- - -models.py#数据表结构目录
 |       |- - -tests.py
 |       |- - -urls.py#后台路由
 |       |- - -views.py/#视图函数逻辑函数
 |       |
 |       |
 |- - -financial/#财务APP
 |       |- - -migrations/#数据库操作日志
 |       |- - -admin.py# django 管理注册
 |       |- - -apps.py
 |       |- - -models.py#表结构
 |       |- - -tests.py#单元测试
 |       |- - -urls.py#后台路由
 |       |- - -views.py/#视图函数逻辑函数
 |
 |- - -homeworks/#数据表结构目录
 |
 |- - -king_admin/#自定义admin
 |       |- - -migrations/#数据库操作日志
 |       |- - -static/#静态文件目录 (备份)
 |       |- - -templates/#HTML文件目录
 |       |     |- - -includes/#load 目录
 |       |     |        |- - -change_list.html#
 |       |     |        |- - -nav-menu.html
 |       |     |- - -kingadmin/#king_admin前端网页目录
 |       |     |        |- - -app_menu.html#单个app的主页面
 |       |     |        |- - -base.html#基础页面
 |       |     |        |- - -index.html#基础主页面
 |       |     |        |- - -page_403.html#错误页面
 |       |     |        |- - -password_reset.html#修改密码页面
 |       |     |        |- - -table_add.html#添加记录页面
 |       |     |        |- - -table_change.html#记录修改页面
 |       |     |        |- - -table_data_list.html#记录列表页面
 |       |     |        |- - -table_del.html#删除记录页面
 |       |     |        |- - -table_index.html#数据表主页面
 |       |- - -templatetags/#注册为模块
 |       |- - -utils/#自定义插件目录
 |       |     |- - -__init__.py
 |       |- - -__init__.py
 |       |- - -admin.py# django 管理注册
 |       |- - -apps.py
 |       |- - -base_admin.py#kingadmin注册类
 |       |- - -forms.py#动态modelsforms表单生成
 |       |- - -models.py#
 |       |- - -tests.py#单元测试
 |       |- - -urls.py#路由
 |       |- - -verify_code.py#验证码函数
 |       |- - -views.py#视图函数
 |
 |- - -sales/#销售APP
 |       |- - -migrations/#数据库操作日志
 |       |- - -admin.py# django 管理注册
 |       |- - -apps.py
 |       |- - -models.py#表结构
 |       |- - -tests.py#单元测试
 |       |- - -urls.py#后台路由
 |       |- - -views.py/#视图函数逻辑函数
 | 
 |
 |- - -static/#静态文件目录
 |       |- - -css/# css文件目录
 |       |- - -enrolled_data/# 身份证上传目录
 |       |- - -imgs/# 图片文件目录
 |       |- - -js/#js文件目录
 |       |- - -plugins/#前端框架文件目录
 |
 |- - -student/#学员APP
 |       |- - -migrations/#数据库操作日志
 |       |- - -admin.py# django 管理注册
 |       |- - -apps.py
 |       |- - -models.py#表结构
 |       |- - -tests.py#单元测试
 |       |- - -urls.py#后台路由
 |       |- - -views.py/#视图函数逻辑函数
 |
 |- - -teacher/#讲师APP
 |       |- - -migrations/#数据库操作日志
 |       |- - -admin.py# django 管理注册
 |       |- - -apps.py
 |       |- - -models.py#表结构
 |       |- - -tests.py#单元测试
 |       |- - -urls.py#后台路由
 |       |- - -views.py/#视图函数逻辑函数
 |
 |
 |- - -templates/#HTML文件目录
 |       |- - -financial/#财务APP页面
 |       |       |- - -contract_review.html#合同审核页面
 |       |       |- - -index_financial.html#财务主页
 |       |       |- - -not_audit.html#驳回页面
 |       |       |- - -payment.html#审核通过页面
 |       |
 |       |- - -include/#include 目录(可包含)
 |       |       |- - -panel-body.html#个人信息模板
 |       |
 |       |- - -master/#母板目录
 |       |       |- - -base.html#后台页面模板
 |       |       |- - -index.html#y主页面模板
 |       |
 |       |- - -sales/#销售APP页面
 |       |       |- - -contract_prompt.html#报名流程 页面
 |       |       |- - -enrollment.html#报名流程一页面
 |       |       |- - -sales_index.html#销售主页
 |       |       |- - -stu_registration.html#学员报名填写页面
 |       |
 |       |- - -student/#学员APP页面
 |       |       |- - -homework_detail.html#作业提交 页面
 |       |       |- - -index.html#学员主页页面
 |       |       |- - -my_course.html#学员班级页面
 |       |       |- - -studyrecords.html#学员班级详情页面
 |       |
 |       |
 |       |- - -teacher/#讲师APP页面
 |       |       |- - -index_teacher.html#讲师主页
 |       |       |- - -teacher_classes_detail.html#讲师详情页面
 |       |       |- - -teacher_classes_detail_howk.html#讲师批改学员作业详情页面
 |       |       |- - -teacher_my_classes.html#讲师所教班级
 |       |
 |       |
 |       |- - -index.html#主页面
 |       |- - -login.html#登陆页面
 |       |- - -modify.html#用户密码修改
 |       |- - -page_403.html#权限提示页面
 |       |- - -register.html#注册页面
 |
 |- - -utils/#自定义插件目录
 |       |- - -check_code.py#验证码
 |       |- - -pagination.py#分页
 |       |- - -xss.py#XSS过滤
 |
 |- - -db.sqlite3/Django自带数据库
 |- - -manage.py#管理Django程序
 |- - -Monaco.ttf#字体库
 |
 |
 |
 |- - -README

```