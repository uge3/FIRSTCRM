#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/10/9    18:32
#__author__='Administrator'
##权限组件#
#url type= 0= related#动态   1= absolute 静态
perm_dic={
   #king_admin
    'crm.can_access_king_admin':{#king_admin 首页
        'url_type':1,
        'url':'/king_admin/',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    # 'crm.can_app_index':{# KING_admin app
    #     'url_type':0,
    #     'url':'app_index',#url name
    #     'method':'GET',#中用于GET
    #     'args':[]
    # },
    'crm.can_access_obj_add':{#kingadmin 信息添加
        'url_type':0,
        'url':'obj_add',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_obj_add_post':{#kingadmin  信息添加post
        'url_type':0,
        'url':'obj_add',#url name
        'method':'POST',#POST
        'args':[]
    },
    'crm.can_table_index':{#kingadmin  单个APP查看
        'url_type':0,
        'url':'table_index',#url name
        'method':'GET',#用于
        'args':[]
    },

    'crm.can_table_list':{#kingadmin  列表查看
        'url_type':0,
        'url':'table_list',#url name
        'method':'GET',#用于
        'args':[]
    },

    'crm.can_access_table_change':{#kingadmin  信息修改
        'url_type':0,
        'url':'table_change',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_table_change_post':{#kingadmin  信息修改post
        'url_type':0,
        'url':'table_change',#url name
        'method':'POST',#POST
        'args':[]
    },

    'crm.can_access_obj_delete':{#kingadmin  信息删除
        'url_type':0,
        'url':'obj_delete',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_obj_delete_post':{#kingadmin  信息删除post
        'url_type':0,
        'url':'obj_delete',#url name
        'method':'POST',#POST
        'args':[]
    },

    'crm.can_access_password_reset':{#kingadmin  修改密码
        'url_type':0,
        'url':'password_reset',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_password_reset_post':{#kingadmin  修改密码post
        'url_type':0,
        'url':'password_reset',#url name
        'method':'POST',#POST
        'args':[]
    },

    #销售
    'crm.can_sales_index':{# 销售首页
        'url_type':0,
        'url':'sales_index',#url name
        'method':'GET',#中用于GET
        'args':[]
    },
    'crm.can_access_customer_list':{# 销售 客户库
        'url_type':1,
        'url':'/king_admin/crm/customer/',#url name
        #'url':'table_list',#url name
        'method':'GET',#只能用GET
        'args':[],
       # 'relist':['/king_admin/crm/customer/']#正则
    },
    'crm.can_access_customer_detail':{# 销售 客户信息详情
        'url_type':2,
        'url':'table_change',#url name
        'method':'GET',#只能用GET
        'args':[],
        'relist':['/king_admin/crm/customer/']#正则
    },
    'crm.can_access_customer_detail_post':{# 销售 客户信息详情
        'url_type':2,
        'url':'table_change',#url name
        'method':'POST',#只能用GET
        'args':[],
        'relist':['/king_admin/crm/customer/']#正则
    },

     'crm.can_access_enrollment':{#报名流程一
            'url_type':0,
            'url':'enrollment',#url name
            'method':'GET',#只能用GET
            'args':[]
        },
    'crm.can_access_enrollment_post':{#报名流程一 post
            'url_type':0,
            'url':'enrollment',#url name
            'method':'POST',#只能用post
            'args':[]
        },

    #讲师
    'crm.can_teacher_index':{#讲师首页
        'url_type':1,
        'url':'/teacher/',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_my_teacher_classes':{#讲师班级
        'url_type':1,
        'url':'/teacher/teacher_my_classes/',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
     'crm.can_teacher_classes_courserecord':{#讲师班级上课
        'url_type':1,
        'url':'/king_admin/crm/courserecord/',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
     'crm.can_teacher_classes_courserecord_post':{#讲师班级上课批量创建
        'url_type':1,
        'url':'/king_admin/crm/courserecord/',#url name
        'method':'POST',#只能用GET
        'args':[]
    },
    'crm.can_teacher_classes_courserecord_change':{#讲师班级课节  信息修改
        'url_type':2,
        'url':'table_change',#url name
        'method':'GET',#只能用GET
        'args':[],
        'relist':['/king_admin/crm/courserecord/']#正则
    },
    'crm.can_teacher_classes_courserecord_change_post':{#讲师班级课节  信息修改post
        'url_type':2,
        'url':'table_change',#url name
        'method':'POST',#POST
        'args':[],
        'relist':['/king_admin/crm/courserecord/']#正则
    },
    'crm.can_teacher_classes_courserecord_add':{#讲师班级上课添加
        'url_type':2,
        'url':'obj_add',#url name
        'method':'GET',#只能用GET
        'args':[],
        'relist':['/king_admin/crm/courserecord/']#正则
    },
    'crm.can_teacher_classes_courserecord_add_post':{#讲师班级上课添加post
        'url_type':2,
        'url':'obj_add',#url name
        'method':'POST',#POST
        'args':[],
        'relist':['/king_admin/crm/courserecord/']#正则
    },
    'crm.can_teacher_classes_studyrecord':{#讲师班级学员上课记录
        'url_type':1,
        'url':'/king_admin/crm/studyrecord/',#url name
        'method':'GET',#POST
        'args':[],
    },
    'crm.can_teacher_classes_studyrecord_post':{#讲师班级学员上课记录 保存
        'url_type':1,
        'url':'/king_admin/crm/studyrecord/',#url name
        'method':'POST',#POST
        'args':[],
    },
     'crm.can_teacher_classes_studyrecord_change':{#讲师班级课节 学习记录
        'url_type':2,
        'url':'table_change',#url name
        'method':'GET',#只能用GET
        'args':[],
        'relist':['/king_admin/crm/studyrecord/']#正则
    },
    'crm.can_teacher_classes_studyrecord_change_post':{#讲师班级课节 学习记录post
        'url_type':2,
        'url':'table_change',#url name
        'method':'POST',#POST
        'args':[],
        'relist':['/king_admin/crm/studyrecord/']#正则
    },



    #财务
    'crm.can_financial_index':{ #财务首页
        'url_type':1,
        'url':'/financial/',#url name
        'method':'GET',#只能用GET
        'args':[]
        },

    'crm.can_financial_not_audit':{ #财务待审核
        'url_type':1,
        'url':'/financial/not_audit/',#url name
        'method':'GET',#只能用GET
        'args':[],#参数
        },

    'crm.can_financial_contract_review':{ #财务审核
        'url_type':0,
        'url':'contract_review',#url name
        'method':'GET',#只能用GET
        'args':[]
        },

    'crm.can_financial_enrollment_rejection':{ #财务驳回
        'url_type':0,
        'url':'enrollment_rejection',#url name
        'method':'GET',#
        'args':[]
        },
    'crm.can_financial_payment':{ #财务缴费
        'url_type':0,
        'url':'payment',#url name
        'method':'GET',#
        'args':[]
        },
    'crm.can_financial_payment_post':{ #财务缴费
        'url_type':0,
        'url':'payment',#url name
        'method':'POST',#
        'args':[]
        },


    #学员
    'crm.can_student_index':{#学员首页
        'url_type':1,
        'url':'/student/',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
     'crm.can_access_my_course':{#学员查看我的课程
        'url_type':0,
        'url':'my_course',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_studyrecords':{#学员学习记录
        'url_type':0,
        'url':'studyrecords',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_homework_detail':{#学员作业详情
        'url_type':0,
        'url':'homework_detail',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_upload_homework':{#学员作业提交
        'url_type':0,
        'url':'homework_detail',#url name
        'method':'POST',#中用于POST
        'args':[]
    },



    #  'crm.can_access_stu_registration':{#报名流程二 学员签同合
    #     'url_type':0,
    #     'url':'stu_registration',#url name
    #     'method':'GET',#只能用GET
    #     'args':[]
    # },









}