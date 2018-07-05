from django.contrib import admin

from .models import Task, TaskList, Tag, SubTask

admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Tag)
admin.site.register(SubTask)
