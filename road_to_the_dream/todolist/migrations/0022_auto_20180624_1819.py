# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 15:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0021_auto_20180623_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 24, 18, 19, 21, 114194)),
        ),
    ]
