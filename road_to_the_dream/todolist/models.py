from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    users = models.ManyToManyField(User, default=None, null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TaskList(models.Model):
    name = models.CharField(max_length=50)
    is_private = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='all_lists', default=None, null=True, blank=True)
    created_user = models.ForeignKey(
        User,
        related_name='created_lists',
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITIES = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
        ('N', 'None')
    )
    STATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('T', 'Trash'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.now(), blank=True)
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    created_user = models.ForeignKey(
        User,
        related_name='created_tasks',
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True)
    completed_user = models.ForeignKey(
        User,
        related_name='completed_tasks',
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, default=None, null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='N')
    status = models.CharField(max_length=1, choices=STATUS, default='P')

    class Meta:
        ordering = ('deadline',)

    def __str__(self):
        return self.title
