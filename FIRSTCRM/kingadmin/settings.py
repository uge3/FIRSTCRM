#_*_coding:utf-8_*_

from django.conf import settings

import os
print(settings.STATICFILES_DIRS,'00011**********')
settings.TEMPLATES[0]['DIRS'] += [os.path.join(settings.BASE_DIR, 'kingadmin/templates')]#加入HTML页面目录

settings.STATICFILES_DIRS +=[ os.path.join(settings.BASE_DIR, 'kingadmin/statics')]#静态目录

print(settings.STATICFILES_DIRS,'kingadmin*************STATICFILES_DIRS')
print(settings.TEMPLATES[0]['DIRS'],'kingadmin settings.TEMPLATES[0]')