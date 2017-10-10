#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/10/3    19:16
#__author__='Administrator'


from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist
from django.utils.timezone import datetime,timedelta
from django.db.models import Sum

register = template.Library()

#分数统计
@register.simple_tag
def get_score(enroll_obj,customer_obj):
    study_records=enroll_obj.studyrecord_set.filter(course_record__from_class_id=enroll_obj.enrolled_class.id)
    print(study_records,'<----study_record')
    return study_records.aggregate(Sum('score'))