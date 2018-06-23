from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField


class Tag(models.Model):
    users = models.ManyToManyField(User, default=None, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TaskList(models.Model):
    name = models.CharField(max_length=50)
    is_private = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='all_lists', default=None, blank=True)
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
        (0, 'High'),
        (1, 'Medium'),
        (2, 'Low'),
        (-1, 'None')
    )
    STATUS = (
        ('P', 'Pending'),
        ('O', 'Overdue'),
        ('C', 'Completed'),
        ('T', 'Trash'),
    )
    DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday '),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    PERIODS = (
        ('D', 'Day'),
        ('W', 'Week'),
        ('M', 'Month'),
        ('Y', 'Year'),
        ('N', 'None')
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
    tags = models.ManyToManyField(Tag, blank=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, default=None, null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='-1')
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    repeat_days = MultiSelectField(max_length=10, max_choices=7, choices=DAYS, null=True, blank=True)
    period_count = models.IntegerField(default=0, blank=True)
    period_val = models.CharField(max_length=1, choices=PERIODS, blank=True, default='N')

    class Meta:
        ordering = ('deadline',)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
    )

    title = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=1, default='P', choices=STATUS)

    def __str__(self):
        return self.title
