from django.contrib import admin, auth


from .models import Task, TaskList, Tag

admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Tag)
