# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-11 16:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0006_auto_20180611_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('N', 'None')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 11, 19, 35, 35, 972676)),
        ),
    ]
