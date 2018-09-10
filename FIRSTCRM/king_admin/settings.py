#_*_coding:utf-8_*_

from django.conf import settings

import os

settings.TEMPLATES[0]['DIRS'] += [os.path.join(settings.BASE_DIR, 'king_admin/templates')]#加入HTML页面目录

settings.STATICFILES_DIRS +=[os.path.join(settings.BASE_DIR, 'king_admin/statics')]#静态目录

