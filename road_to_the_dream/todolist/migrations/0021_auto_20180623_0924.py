# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 06:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0020_auto_20180621_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 23, 9, 24, 58, 315641)),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[(0, 'High'), (1, 'Medium'), (2, 'Low'), (-1, 'None')], default='-1', max_length=1),
        ),
    ]
