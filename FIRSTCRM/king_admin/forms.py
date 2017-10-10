
from django import forms
from django.forms import ModelForm,ValidationError
from django.utils.translation import ugettext as _ #国际化



#
# class CustomerModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Customer
#         fields = "__all__"

#动态生成modelform
def CreateModelForm(request,admin_obj):#传入前端提交的表单
    class Meta:
        model = admin_obj.model#传入表结构对象
        # if admin_obj.readonly_fields:
        #     exclude = admin_obj.readonly_fields
        #else:
        fields = "__all__"
        exclude= admin_obj.modelform_exclude_fields#排除不需要验证的字段

    #重写 函数生成方法
    def __new__(cls, *args, **kwargs):#重写 函数生成方法
        #print("base fields",cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'#前端的样式
            if not hasattr(admin_obj,"is_add_form"):#如果不是为新增表单
                if field_name in admin_obj.readonly_fields:#如果加入 列表, 表示不可修改
                    field_obj.widget.attrs['disabled'] = True


            #clean_func='clean_%s'%field_name#拼接字段的单独验证的函数名
            # if hasattr(admin_obj,'clean_%s'%field_name):#是否有该字段的单独验证
            #     field_clean_func=getattr(admin_obj,'clean_%s'%field_name)#获取对应的函数
            #
            #     # if kwargs:
            #     print(field_obj.widget.attrs,'+++++++++++++++',cls.base_fields)
            #     print(field_clean_func,'----****对应的函数',args,'&&&&&&&&&',kwargs)
            #     for i in kwargs:
            #         print(i)
            #     #print('cls',cls.base_fields.data)
            #     #     print(type(kwargs),type(admin_obj))
            #     #cls.cleaned_data=kwargs#加入数据
            #     #print(cls.cleaned_data)
            #     setattr(cls,'clean_%s'%field_name,field_clean_func)#添加该函数
                #clean_func='clean_%s'%field_name


        return forms.ModelForm.__new__(cls)

    def clean_all(self):
        print(self)

    def default_clean(self):
        print("default clean:",type(self.instance))
        print("default clean:",self.instance)
        error_list=[]
        if admin_obj.readonly_table:
            raise ValidationError(#添加错误信息
                                    _("该表单不可修改!"),
                                    code='invalid',
                                )
        if self.instance.id:#表示为修改表单
            for field in admin_obj.readonly_fields:#如果是不可修改的字段
                print("readonly",field,self.instance)
                #field_val_from_db = getattr(self.instance,field)#取数据库中的值
                field_val_from_db = getattr(self.instance,field)#取数据库中的值
                field_val = self.cleaned_data.get(field)#前端传来的值
                if hasattr(field_val_from_db,'select_related'):#多对多
                    m2m_objs=getattr(field_val_from_db,'select_related')().select_related()#调用多对多,获取对应的值
                    m2m_vals=[i[0] for i in m2m_objs.values_list('id')]#转为列表
                    set_m2m_vals=set(m2m_vals)#转集合  交集 数据库

                    # vals_from_frontend=self.cleaned_data.get(field)#前端的值  交集
                    # m2m_vals=[i[0] for i in vals_from_frontend.values_list('id')]#转为列表
                    # print(vals_from_frontend,'前端的值  交集',m2m_vals)
                    set_m2m_vals_from_frontend=set([i.id for i in self.cleaned_data.get(field)])#前端的值  交集

                    if set_m2m_vals != set_m2m_vals_from_frontend:
                        error_list.append(ValidationError(
                            _("%(field)s: 该字段不可修改!"),
                                    code='invalid',
                                    params={'field':field,}
                        ))
                        self.add_error(field,"不可修改!")
                    continue

                #field_val = self.cleaned_data.get(field)#前端传来的值
                print('field_val',type(field_val))
                if field_val_from_db != field_val:
                    print("field not change ")#不一致
                    error_list.append(ValidationError(#添加错误信息
                                    _("该字段%(field)s 不可修改,原值为: %(val)s"),
                                    code='invalid',
                                    params={'field':field,'val':field_val_from_db}
                                ))

                # else: # 被篡改了
                #     self.add_error(field,' "%s" is a readonly field ,value should be "%s" '% (field, field_val_from_db))

        print("cleaned data:",self.cleaned_data,)#要验证的表单
        for field in self.cleaned_data:#单独字段
            if hasattr(admin_obj,'clean_%s'%field):#是否有该字段的单独验证
                field_clean_func=getattr(admin_obj,'clean_%s'%field)#获取对应的函数
                print('-------------||||||||----------------')
                response=field_clean_func(self)#
                if response:
                    error_list.append(response)
                if error_list:
                    raise ValidationError(error_list)
                #response_sol=admin_obj.('clean_%s'%field)(self.cleaned_data)

        # if hasattr(admin_obj,'default_form_validation'):
        #     print(admin_obj.default_form_validation,':::::::::::::::::')
        response=admin_obj.default_form_validation(self)#可自定制
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)

    dynamic_model_form = type("DynamicModelForm",(forms.ModelForm,), {"Meta":Meta})#生成modelform的类,

    setattr(dynamic_model_form,"__new__",__new__)
    setattr(dynamic_model_form,"clean",default_clean)
    return dynamic_model_form