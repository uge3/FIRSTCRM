

from king_admin import custom_perm_logic


perm_dic={

    'crm_app_index':['app_index','GET',[],{},],  #可以查看CRM APP里所有数据库表
    'crm_table_list':['table_list','GET',[],{},
                      custom_perm_logic.only_view_own_customers],    #可以查看每张表里所有的数据
    'crm_table_list_view':['table_change','GET',[],{}],#可以访问表里每条数据的修改页
    'crm_table_list_change':['table_change','POST',[],{}], #可以对表里的每条数据进行修改

    }

