from datetime import datetime
from dateutil.relativedelta import *

from .models import Task, SubTask
from django.db.models import Q
from django.utils import timezone


def check_overdue():
    tasks = Task.objects.filter(Q(status='O') | Q(status='P'))
    for task in tasks:
        if task.deadline:
            if task.created_user.username == 'kek':
                print(task.deadline, timezone.now(), task.deadline > timezone.now())
            if task.deadline > timezone.now():
                task.status = 'P'
            else:
                task.status = 'O'
            task.save()


def checkable(foo):
    def wrapper(*args, **kwargs):
        print('hi')
        check_overdue()
        return foo(*args, **kwargs)
    return wrapper


def complete_task(task, user):
    check_overdue()
    if task.period_val and task.period_val != 'N' and task.period_val != '':
        for st in task.subtask_set.all():
            st.status = 'P'
        if task.period_val == 'D':
            task.deadline += relativedelta(days=+task.period_count)
        elif task.period_val == 'W':
            if task.repeat_days and len(task.repeat_days):
                last_weekday = task.deadline.weekday()
                days = [MO, TU, WE, TH, FR, SA, SU]
                new_week = True
                for day in task.repeat_days:
                    print('day:', day, last_weekday)
                    if int(day) - 1 > last_weekday:
                        new_week = False
                        task.deadline += relativedelta(weekday=days[int(day)-1])
                        break
                if new_week:
                    first_day_number = int(task.repeat_days[0]) - 1
                    task.deadline += relativedelta(weeks=task.period_count - 1, weekday=days[first_day_number])
            else:
                task.deadline += relativedelta(weeks=+task.period_count)
        elif task.period_val == 'M':
            task.deadline += relativedelta(months=+task.period_count)
        elif task.period_val == 'Y':
            task.deadline += relativedelta(years=+task.period_count)
    else:
        for st in task.subtask_set.all():
            st.status = 'C'
        task.completed_user = user
        task.status = 'C'
    return task


def validate_data(title, description, tags, priority, list_id, deadline, period, days, count):
    pass
