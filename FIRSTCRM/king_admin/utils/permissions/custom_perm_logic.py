import re
def only_view_own_customers(request ,*args ,**kwargs):
    print('perm test' ,request ,args ,kwargs)

    consultant_id = request.GET.get('consultant')
    if consultant_id:
        consultant_id = int(consultant_id)

    print("consultant=1" ,type(consultant_id))

    if consultant_id == request.user.id:
        print( "\033[31;1mchecking [%s]'s own customers, pass..\033[0m"% request.user)
        return True
    else:
        print("\033[31;1muser can only view his's own customer...\033[0m")
        return False

#讲师查看自班级表GET
def my_all_class(request ,*args ,**kwargs):#
    url_path=request.path #获取URL
    print(url_path)
    print('perm test' ,request ,args ,kwargs)
    url_list=re.findall('(\w+)',url_path) #取URL
    url_model_name=url_list[2]
    model_name = 'classlist'
    if url_model_name == model_name: #防止其他表通过权限
        teacher_id=request.GET.get('teacher')#讲师的过滤条件
        if teacher_id:
            teacher_id=int(teacher_id)#对应的讲师ID转数整型
            if teacher_id==request.user.id:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

#讲师查看自已的单班级详情GET
def my_class_detail(request ,*args ,**kwargs):#
    url_path=request.path #获取URL
    print(url_path)
    print('perm test' ,request ,args ,kwargs)
    url_list=re.findall('(\w+)',url_path) #取URL
    url_model_name=url_list[2]
    model_name = 'courserecord'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False

#010201_只能查看校区表_GET
def see_Branch(request,*args,**kwargs):
    url_path = request.path  # 获取URL
    url_list=re.findall('(\w+)',url_path) #正者表达式 获取参数
    url_model_name=url_list[2]

    model_name = 'branch'
    if url_model_name == model_name: #防止其他表通过权限
        return True
    else:
        return False