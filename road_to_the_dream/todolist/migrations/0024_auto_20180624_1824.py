# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0023_auto_20180624_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('0', 'High'), ('1', 'Medium'), ('2', 'Low'), ('-1', 'None')], default='-1', max_length=1),
        ),
    ]
