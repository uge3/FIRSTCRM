# ECJ.py
# ————————75PerfectCRM实现CRM扩展权限————————
import re #正则

#070101_查看自己的客户表_GET
def view_own_Customer(request,*args,**kwargs):
    url_path = request.path #获取URL 路径
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name= url_list[2] #字符串
    model_name = 'customer'#字符串
    if url_model_name==model_name: #防止其他表通过权限
        consultant_id = request.GET.get('consultant') #过滤条件 &consultant=7
        if consultant_id:
            consultant_id = int(consultant_id) #转换成 数字
        if consultant_id == request.user.id: # 账号表 的ID 等于 #当前登陆的ID
            return True
        else:
            return False
    else:
        return False

#070103_修改自己的客户表_GET
#070105_删除自己的客户表_GET
def change_own_Customer(request,*args,**kwargs):
    url_path = request.path #获取URL 路径
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name= url_list[2]
    url_parameter =int(url_list[3])
    model_name = 'customer'
    if url_model_name==model_name: #防止其他表通过权限
        if request.user.id: #如果有ID
            list= request.user.customer_set.all()#获取ID 的客户表
            list_id=[]
            for obtain in list:#循环客户表ID
                results=obtain.id
                list_id.append(results)#生成列表
        if url_parameter in list_id: #对比URL参数 在不在 客户表ID里
            return True
        else:
            return False
    else:
        return False

# ————————75PerfectCRM实现CRM扩展权限————————
