# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20170928_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='合同名称')),
                ('template', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='id_num',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='身份证号'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sex',
            field=models.SmallIntegerField(choices=[(0, '保密'), (1, '男'), (2, '女')], default=0, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ContractTemplate'),
        ),
    ]
