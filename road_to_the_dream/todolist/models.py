from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TaskList(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITIES = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
        ('N', 'None')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.now(), blank=True)
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, default=None, null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='N')

    class Meta:
        ordering = ('deadline',)

    def __str__(self):
        return self.title



