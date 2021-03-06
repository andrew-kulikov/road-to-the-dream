# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-12 11:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0007_auto_20180611_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 12, 14, 3, 16, 241250)),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('T', 'Trash')], default='P', max_length=1),
        ),
    ]
