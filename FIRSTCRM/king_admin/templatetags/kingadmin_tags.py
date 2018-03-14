
from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist
from django.utils.timezone import datetime,timedelta
from django.db.models.query import QuerySet
register = template.Library()

#表的记录数据
@register.simple_tag
def get_query_sets(admin_clss):#传入表类 的对象
    return admin_clss.model.objects.all()#获取所有变量名

#自定义标签
@register.simple_tag
def get_model_verbose_name(model_obj):
    #
    model_name = model_obj._meta.verbose_name if model_obj._meta.verbose_name else model_obj._meta.verbose_name_plural

    if not model_name:
        model_name = model_obj._meta.model_name

    print("model obj",model_name)
    return model_name


#表的名字
@register.simple_tag
def get_model_name(model_obj):
    return model_obj._meta.model_name

#app的名字
@register.simple_tag
def get_app_name(model_obj):
    return model_obj._meta.app_label


@register.simple_tag
def print_obj(obj):
    print("DEBUG:::",obj)
    print("DEBUG:::",dir(obj))


#分页的省略显示
@register.simple_tag
def pag_omit(request,admin_obj):#传入当前页面值
    rest=''#大字符串
    order_by_url=generate_order_by_url (request)#排序
    filters=generate_filter_url(admin_obj)# 搜索 条件
    search_key=get_search_key(request)#关键字
    add_tags=False#标志位
    for  pages in admin_obj.querysets.paginator.page_range:
        #   前两页    或   后  两页                                       或    当前页的前后页
        if pages < 3 or pages>admin_obj.querysets.paginator.num_pages -2 or abs(admin_obj.querysets.number -pages) <=2:
            #样式
            add_tags=False
            ele_class=''
            if pages == admin_obj.querysets.number: #--如果是当前页码,颜色加深 不进链接跳转--
                ele_class="active"
            rest+='''<li class="%s"><a href="?page=%s%s%s&_q=%s">%s<span class="sr-only">(current)</span></a></li>'''\
                    %(ele_class,pages,filters,order_by_url,search_key,pages)
        else:
            if add_tags==False:#如果不是标志位的页面
                rest+='<li><a>...</a></li>'
                add_tags=True#标志位为真
    return mark_safe(rest)

#表中列名
@register.simple_tag
def build_table_row(admin_obj,obj):
    row_ele = ""#定义 一个空字符串
    column_not=[]#表示不是表中字段列表
    if admin_obj.list_display:# 如果有自定义的列名
        for index,column in enumerate(admin_obj.list_display):#转为列表取 下标 , 字段名
            try:
                column_obj = obj._meta.get_field(column)#取到数据类型
                if column_obj.choices:#判断是否是 choices字段
                    get_column_data = getattr(obj,"get_%s_display" % column)#查找对应的选择
                    column_data = get_column_data()#执行方法
                else:
                    column_data = getattr(obj, column)
                if type(column_data).__name__=='datetime':#如果是日期格式
                    column_data=column_data.strftime('%Y-%m-%d %H-%M-%S')
                if index == 0: #首列
                    #生成一个链接 跳转到编辑页面
                    td_ele = '''<td><a href="/king_admin/{app_name}/{model_name}/{obj_id}/change/">{column_data}</a> </td>'''\
                                .format(app_name=admin_obj.model._meta.app_label,#APP名
                                        model_name=admin_obj.model._meta.model_name,#表名
                                        obj_id=obj.id,column_data=column_data)#日期格式
                else:
                    td_ele = '''<td>%s</td>''' % column_data
                admin_obj.column_not=False#表示是表中字段

            except FieldDoesNotExist as e: #如果没有获取到
                if hasattr(admin_obj,column):#从自定义的函数中取值
                    column_func=getattr(admin_obj,column)#
                    admin_obj.instance=obj#对象加入

                    column_not.append(column)#加入非表中字段列表,
                    admin_obj.column_not=column_not#对象加入
                    column_data=column_func()
                    print('column_data',column_data)
                    td_ele = '''<td>%s</td>''' % column_data
            row_ele += td_ele
    else:
        row_ele += "<td>%s</td>" % obj#用<tb>标签包
    return mark_safe(row_ele)#返回前端字符串


##表中自定verbose_name列名
@register.simple_tag
def verbose_name_set(admin_obj,column):
    try:
        verbose_name=admin_obj.model._meta.get_field(column).verbose_name.upper()#获取别名
        print(verbose_name,'verbose_name_set')
        print(admin_obj.model._meta,'all')
    except FieldDoesNotExist as e:
        verbose_name=getattr(admin_obj,column).display_name.upper()
    return verbose_name



#过滤条件
@register.simple_tag
def get_filter_field (filter_column,admin_obj):#过滤条件
    print("admin obj",admin_obj.model ,filter_column)
    field_obj = admin_obj.model._meta.get_field(filter_column)
    select_ele = """<select class="form-control" name='{filter_column}'><option class="form-control" value="">---------</option>""" #标签 字符串
    #if type(field_obj).__name__=='ForeignKey':

    if type(field_obj).__name__ in ['DateTimeField','DateField']:#如果是时间格式
        date_els=[]#日期条件项
        today_ele=datetime.now().date()#今天日期
        date_els.append(['today_ele',today_ele])#今天
        date_els.append(['yesterday_ele',today_ele-timedelta(days=1)])#昨天
        date_els.append(['last7day_ele',today_ele-timedelta(days=7)])#一周
        date_els.append(['last30day_ele',today_ele-timedelta(days=30)])#三十
        date_els.append(['mtdy_ele',today_ele.replace(day=1)])#本月
        date_els.append(['last90day_ele',today_ele-timedelta(days=90)])#90天
        date_els.append(['last365day_ele',today_ele-timedelta(days=365)])#365天
        date_els.append(['ytd_ele',today_ele.replace(month=1,day=1)])##今年

        for item in date_els:
            selected_condtion = admin_obj.filter_condtions.get(filter_column)
            if selected_condtion != None: #if None, 没有过滤这个条件
                print("heoe....",filter_column,selected_condtion,type(selected_condtion))
                if selected_condtion == str(item[1]): #就是选择的这个条件
                    selected = "selected"
                else:
                    selected = ""
            else:
                selected = ""
            option_ele = """<option value="%s" %s>%s</option> """ % (item[1],selected,item[0])#选中的条件
            select_ele +=option_ele
        filter_column_name="%s__gte"%filter_column
    else:
        for choice in field_obj.get_choices():#如果是choices
            selected_condtion = admin_obj.filter_condtions.get(filter_column)
            if selected_condtion != None: #if None, 没有过滤这个条件
                print("heoe....",filter_column,selected_condtion,type(selected_condtion))
                if selected_condtion == str(choice[0]): #就是选择的这个条件
                    selected = "selected"
                else:
                    selected = ""
            else:
                selected = ""
            option_ele = """<option class="form-control" value="%s" %s>%s</option> """ % (choice[0],selected,choice[1])#选中的条件
            select_ele +=option_ele
        filter_column_name=filter_column
    select_ele += "</select>"
    select_ele=select_ele.format(filter_column=filter_column_name)#格式化时间的判断条件
    return mark_safe(select_ele)

#过滤的条件URL
@register.simple_tag
def generate_filter_url(admin_obj):#过滤的条件值
    url = ''
    for k,v in admin_obj.filter_condtions.items():
        url += "&%s=%s" %(k,v )
    return url

#排序 生成使用
@register.simple_tag
def  get_orderby_key(request,column):
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None: #肯定有某列被排序了
        if current_order_by_key ==  column: # 当前这列正在被排序
            if column.startswith("-"):
                return column.strip("-")
            else:
                return "-%s"%column
    return column

#被排序了key
@register.simple_tag
def get_current_orderby_key(request):
    #获取当前正在排序的字段名
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key == None: #如果没有某列被排序了
        return  ''
    return current_order_by_key

#被排序了值 url 分页使用
@register.simple_tag
def generate_order_by_url (request):
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None:  # 肯定有某列被排序了
        return "&_o=%s" % current_order_by_key#返回对应的内容
    return ''

#关键字搜索
@register.simple_tag
def get_search_key(request):
    return request.GET.get("_q") or ''

#排序的图标
@register.simple_tag
def display_order_by_icon(request, column):
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None: #肯定有某列被排序了 如果没有
        if current_order_by_key.strip("-") == column: ## 当前这列正在被排序
            if current_order_by_key.startswith("-"):#如果是负排
                icon = "fa-arrow-up"
            else:
                icon = "fa-arrow-down"
            ele = """<i class="fa %s" aria-hidden="true"></i>""" % icon
            return mark_safe(ele)
    return ''#如果没有为空

#自定制 actions功能 显示
@register.simple_tag
def get_admin_actions(admin_obj):
    #选择功能
    options = "<option class='form-control' value='-1'>-------</option>"#默认为空
    actions = admin_obj.default_actions + admin_obj.actions #默认加自定制
    print('默认加自定制',actions)
    for action in actions:
        action_func = getattr(admin_obj,action)#功能方法
        if hasattr(action_func,"short_description"):#反射 如有自定义的名称执行函数方法
            action_name = action_func.short_description#等于自定义的名称
        else:
            action_name = action#等于函数名称
        options += """<option value="{action_func_name}">{action_name}</option> """.format(action_func_name=action,
                                                                                           action_name=action_name)
    return mark_safe(options)

#复选 框内容待选数据
@register.simple_tag
def get_m2m_available_objs (admin_obj,field_name):
    '''返回m2m左侧所有待选数据'''
    m2m_model = getattr(admin_obj.model,field_name).rel.to#复选框对象
    m2m_objs = m2m_model.objects.all()#获取到复选框所有内容
    return m2m_objs

#复选 框内容已选中数据
@register.simple_tag
def get_m2m_chosen_objs (admin_obj, field_name,obj):
    """
    返回已选中的列表
    :param admin_obj:
    :param field_name:
    :param obj: 数据对象
    :return:
    """
    print(["--->obj",obj])
    if obj.id:
        return getattr(obj,field_name).all()#返回所有的内容
    return []#没有数据为返回空   创建新的记录使用



#删除记录
@register.simple_tag
def display_all_related_obj(objs):
    #取出对象及所有相关联的数据
    #print(type(objs),'objs==----')
    if type(objs)!=QuerySet:#如果不是批量选择
        objs=[objs,]
    if objs:
        model_class=objs[0]._meta.model#取表对象
        model_name=objs[0]._meta.model_name#取表名
        return mark_safe(recursive_related_objs_lookup(objs))

#删除 显示内容拼接
def recursive_related_objs_lookup(objs,name=None,conn_batch_size=0):
    model_name=objs.__str__()#取表名#递归时使用
    print(model_name,'model-name')
    #name = objs[0]._meta.model_name
    name=set()
    ul_ele="<ul>"
    for obj in objs:
        #                                         关联的表的自定表名
        li_ele='''<li>%s:%s</li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele+=li_ele
        #多对多
        for m2m_field in obj._meta.local_many_to_many:#如果有多对多字段
            sub_ul_ele='<ul>'
            m2m_field_obj=getattr(obj,m2m_field.name)#反射 如果有选项
            for o in m2m_field_obj.select_related():#循环输出 拼接
                li_ele='''<li>%s:%s</li>'''%(m2m_field.verbose_name,o.__str__().strip("<>"))
                sub_ul_ele+=li_ele
            sub_ul_ele+="</ul>"
            ul_ele +=sub_ul_ele#外层的UL 拼接

        #多对一 外键
        for related_obj in obj._meta.related_objects:#相关联的外键表
            if "ManyToManyRel" in related_obj.__repr__():#如果是多对多的关系 外
                if hasattr(obj,related_obj.get_accessor_name()):#反射 如果有相关的方法
                    accessor_obj=getattr(obj,related_obj.get_accessor_name())#取出表名
                    if hasattr(accessor_obj,'select_related'):#如果有外键关联选项 select_related()==all()
                        target_objs=accessor_obj.select_related()#取出所有外键相关联
                        sub_ul_ele='<ul style="color:red">'
                        for o in target_objs:#循环输出 拼接
                            li_ele='''<li>%s:%s</li>'''%(o._meta.verbose_name,o.__str__().strip("<>"))
                            sub_ul_ele+=li_ele
                        sub_ul_ele+="</ul>"
                        ul_ele +=sub_ul_ele#外层的UL 拼接
            elif hasattr(obj,related_obj.get_accessor_name()):#反射 如果有相关的方法
                accessor_obj=getattr(obj,related_obj.get_accessor_name())#取出表名
                if hasattr(accessor_obj,'select_related'):#如果有外键关联选项 select_related()==all()
                    target_objs=accessor_obj.select_related()#取出所有外键相关联
                else:
                    target_objs=accessor_obj
                # if len(target_objs)>0:#如果还有下层
                if len(target_objs)!=conn_batch_size:#如果还有下层
                    names=target_objs.__str__()
                    if names==model_name:#如果是自己关联自己，就不递归了
                        ul_ele+="</ul>"
                    else:
                        conn_batch_size=conn_batch_size+1
                        # nodes=recursive_related_objs_lookup(target_objs)#递归
                        nodes=recursive_related_objs_lookup(target_objs,name=model_name,conn_batch_size=conn_batch_size)#递归
                        ul_ele+=nodes
    ul_ele+="</ul>"
    return ul_ele



