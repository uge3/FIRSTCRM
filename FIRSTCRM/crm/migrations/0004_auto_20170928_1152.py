# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 03:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_userprofile_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='contract_url',
            field=models.TextField(null=True, verbose_name='学员合同确认链接'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='客户'),
        ),
    ]
