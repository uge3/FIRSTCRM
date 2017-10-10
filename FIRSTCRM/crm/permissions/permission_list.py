#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/10/9    18:32
#__author__='Administrator'
##权限组件#
#url type= 0= related#动态   1= absolute 静态
perm_dic={
    'crm.can_access_my_course':{#查看我的班级
        'url_type':0,
        'url':'my_classes',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_customer_list':{#客户库
        'url_type':1,
        'url':'king_admin/crm/customer/',#url name
        'method':'GET',#只能用GET
        'args':[]
    },
    'crm.can_access_customer_detail':{#客户信息详情
        'url_type':0,
        'url':'table_change',#url name
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

}