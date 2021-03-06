# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 16:19
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0014_auto_20180615_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 6, 15, 19, 19, 57, 55041)),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, to='todolist.Tag'),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='users',
            field=models.ManyToManyField(blank=True, default=None, related_name='all_lists', to=settings.AUTH_USER_MODEL),
        ),
    ]
