#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/9/28    21:50
#__author__='Administrator'

from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist
from django.utils.timezone import datetime,timedelta

register = template.Library()

#合同格式
@register.simple_tag
def render_enrolled_contract(enroll_obj):#合同格式
    if enroll_obj.enrolled_class.contract.template:
        return enroll_obj.enrolled_class.contract.template.format(course_name=enroll_obj.enrolled_class,stu_name=enroll_obj.customer.name)
    else:
        return ''
    # return enroll_obj.enrolled_class.contract.template.format(course_name=enroll_obj.enrolled_class,stu_name=enroll_obj.customer.name)

#驳回
@register.simple_tag
def enrollment_rejection(enroll_id):
    return