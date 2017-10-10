#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#FIRSTCRM 
#2017/9/28    9:27
#__author__='Administrator'


from crm import models
from django.shortcuts import render
from django.forms import ModelForm,ValidationError
from django.utils.translation import ugettext as _ #国际化

#报名 销售填写
class EnrollmentForm(ModelForm):

    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'## 前端的样式
        return ModelForm.__new__(cls)

    class Meta:
        model= models.Enrollment
        fields= ['enrolled_class','consultant']

#缴费记录
class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'## 前端的样式
        return ModelForm.__new__(cls)

    class Meta:
        model=models.Payment
        fields='__all__'


#报名学员填 写
class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'## 前端的样式
            if field_name in cls.Meta.readonly_fields:#如果不可修改
                field_obj.widget.attrs['disabled'] = True## 前端的样式 灰色
        return ModelForm.__new__(cls)

    def clean_qq(self):
        print(self.instance.qq,self.cleaned_data['qq'],'9696969696')
        if self.instance.qq != self.cleaned_data['qq']:
            self.add_error('qq',"非法修改！")
        return self.cleaned_data['qq']

    def clean_consultant(self):
        if self.instance.consultant != self.cleaned_data['consultant']:
            self.add_error('consultant',"非法修改！")
        return self.cleaned_data['consultant']

    def clean_source(self):
        if self.instance.source != self.cleaned_data['source']:
            self.add_error('source',"非法修改！")
        return self.cleaned_data['source']

    class Meta:
        model=models.Customer#客户表
        fields='__all__'
        exclude=['tags','content','memo','status','referral_from','consult_course']#排除，不显示
        readonly_fields=['qq','consultant','source']#不可修改

