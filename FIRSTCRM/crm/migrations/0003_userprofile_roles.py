# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-27 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20170927_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='crm.Role'),
        ),
    ]
