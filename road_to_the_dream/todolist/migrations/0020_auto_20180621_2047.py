# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-21 17:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0019_auto_20180616_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 21, 20, 47, 57, 838050)),
        ),
        migrations.AlterField(
            model_name='task',
            name='period_val',
            field=models.CharField(blank=True, choices=[('D', 'Day'), ('W', 'Week'), ('M', 'Month'), ('Y', 'Year'), ('N', 'None')], default='N', max_length=1),
        ),
    ]
