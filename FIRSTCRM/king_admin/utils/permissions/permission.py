from django.conf import settings
# from django.core.urlresolvers import resolve
from django.urls import resolve
from django.shortcuts import render,redirect
from king_admin.utils.permissions.ECJ import * #扩展的自定义函数
from king_admin.utils.permissions.permission_list import perm_dic


def perm_check(*args,**kwargs):

    request = args[0]
    resolve_url_obj = resolve(request.path)#解析URL 用于#绝对URL转成动态的URLname
    current_url_name = resolve_url_obj.url_name  # 当前url的url_name
    # print('---perm:',request.user,request.user.is_authenticated(),current_url_name)
    #match_flag = False
    match_key = None
    match_results = [False,] #后面会覆盖，加个False是为了让all(match_results)不出错
    if request.user.is_authenticated is False:
         return redirect(settings.LOGIN_URL)

    for permission_key,permission_val in  perm_dic.items():#从权限字典中取相关字段

        per_url_name = permission_val[0]
        per_method  = permission_val[1]
        perm_args = permission_val[2]
        perm_kwargs = permission_val[3]
        custom_perm_func = None if len(permission_val) == 4 else permission_val[4]#是否有第五个字段

        if per_url_name == current_url_name: #matches current request url
            if per_method == request.method: #matches request method
                # if not  perm_args: #if no args defined in perm dic, then set this request to passed perm check
                #     match_flag = True
                #     match_key = permission_key
                # else:

                #逐个匹配参数，看每个参数时候都能对应的上。
                args_matched = False #for args only
                for item in perm_args:
                    request_method_func = getattr(request,per_method)
                    if request_method_func.get(item,None):# request字典中有此参数
                        args_matched = True
                    else:
                        print("arg not match......")
                        args_matched = False
                        break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                else:
                    args_matched = True
                #匹配有特定值的参数
                kwargs_matched = False
                for k,v in perm_kwargs.items():
                    request_method_func = getattr(request, per_method)
                    arg_val = request_method_func.get(k, None)  # request字典中有此参数
                    print("perm kwargs check:",arg_val,type(arg_val),v,type(v))
                    if arg_val == str(v): #匹配上了特定的参数 及对应的 参数值， 比如，需要request 对象里必须有一个叫 user_id=3的参数
                        kwargs_matched = True
                    else:
                        kwargs_matched = False
                        break # 有一个参数不能匹配成功，则判定为假，退出该循环。
                else:
                    kwargs_matched = True

                #自定义权限钩子
                perm_func_matched = False
                if custom_perm_func:
                    if  custom_perm_func(request,args,kwargs):
                        perm_func_matched = True
                    else:
                        perm_func_matched = False #使整条权限失效

                else: #没有定义权限钩子，所以默认通过
                    perm_func_matched = True

                match_results = [args_matched,kwargs_matched,perm_func_matched]
                print("--->match_results ", match_results)
                if all(match_results): #都匹配上了
                    match_key = permission_key
                    break


    if all(match_results):
        app_name, *per_name = match_key.split('_')
        print("--->matched ",match_results,match_key)
        print(app_name, *per_name)
        perm_obj = '%s.%s' % (app_name,match_key)
        print("perm str:",perm_obj)
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False

    else:
        print("未匹配到权限项，当前用户无权限")
        return False

#装饰器函数
def check_permission(func):
    def inner(*args,**kwargs):#'开始权限匹配
        request = args[0]
        if request.user.is_admin == True:
            print('超级管理员')
            return func(*args, **kwargs)  # 直接返回 真
        if not perm_check(*args,**kwargs):
            # request = args[0]
            return render(request, 'king_admin\page_403.html')
        return func(*args,**kwargs)
    return  inner

