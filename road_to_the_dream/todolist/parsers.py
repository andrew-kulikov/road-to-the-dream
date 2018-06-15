from datetime import datetime

from .models import Task
from django.db.models import Q
from django.utils import timezone


def check_overdue():
    tasks = Task.objects.filter(Q(status='O') | Q(status='P'))
    for task in tasks:
        if task.deadline:
            if task.deadline > timezone.now():
                task.status = 'P'
            else:
                task.status = 'O'
            task.save()

