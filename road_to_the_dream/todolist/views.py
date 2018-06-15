from datetime import datetime, date, timedelta

from dateutil.relativedelta import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from . import parsers
from .models import Task, TaskList, Tag, SubTask


@login_required(login_url='/accounts/login')
def index(request):
    parsers.check_overdue()
    tasks = Task.objects.filter(Q(created_user=request.user) & Q(status='P') | Q(status='O'))
    task_lists = TaskList.objects.filter(users__in=[request.user])
    tags = Tag.objects.all()
    context = {
        'tasks': tasks,
        'task_lists': task_lists,
        'tags': tags
    }
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login')
def details(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        if task.status == 'C':
            task.status = 'P'
            task.save()
            parsers.check_overdue()
        
        title = request.POST['subtask_name']
        st = SubTask(title=title, task=task)
        st.save()
    context = {
        'task': task,
        'completed': request.META.get('HTTP_REFERER') == 'http://localhost:8000/todolist/lists/completed/'
    }
    return render(request, 'details.html', context)


@login_required(login_url='/accounts/login')
def list_details(request, list_id):
    list = TaskList.objects.get(id=list_id)
    tasks = list.task_set.filter(status='P')
    users = list.users.all()
    context = {
        'tasks': tasks,
        'users': users,
        'list': list,
        'superuser': request.user.is_superuser
    }
    return render(request, 'list_details.html', context)


@login_required(login_url='/accounts/login')
def tag_details(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    tasks = tag.task_set.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'tag_details.html', context)


@login_required(login_url='/accounts/login')
def add(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        tags = request.POST.getlist('tags')
        priority = request.POST['priority']
        list_id = request.POST['list_id']
        deadline = request.POST['deadline']
        period = request.POST['period']
        days = request.POST.getlist('days')
        dd = None
        if deadline != '':
            dd = datetime.strptime(deadline, '%m/%d/%Y %I:%M %p')
        user = request.user
        task = Task(
            title=title,
            description=description,
            created_user=user,
            priority=priority,
            deadline=dd,
            task_list_id=int(list_id)
        )
        if dd:
            task.period_val = period
            task.period_count = 1
            if period == 'W':
                task.repeat_days = days
        task.save()
        for tag in tags:
            task.tags.add(Tag.objects.get(id=int(tag)))
            task.save()

        return redirect('/todolist')
    return render(request, 'add.html')


@login_required(login_url='/accounts/login')
def add_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        is_private = False
        if 'is_private' in request.POST:
            is_private = True
        user = request.user
        tasklist = TaskList(name=name, is_private=is_private, created_user=user)
        tasklist.save()
        tasklist.users.add(user)
        tasklist.save()
        return redirect('/todolist')
    return render(request, 'add_tasklist.html')


@login_required(login_url='/accounts/login')
def add_tag(request):
    if request.method == 'POST':
        name = request.POST['name']
        user = request.user
        tag = Tag(name=name)
        tag.save()
        tag.users.add(user)
        tag.save()
        return redirect('/todolist')
    return render(request, 'add_tag.html')


@login_required(login_url='/accounts/login')
def edit_list(request, list_id):
    if request.method == 'POST':
        name = request.POST['name']
        is_private = 'is_private' in request.POST
        user = request.user
        try:
            tasklist = TaskList.objects.get(id=list_id, created_user=user)
            tasklist.name = name
            tasklist.is_private = is_private
            tasklist.save()
            if is_private:
                tasklist.users.clear()
                tasklist.users.add(user)
                tasklist.save()
        except Exception as e:
            messages.warning(request, 'Ti ne admin')
        return redirect('/todolist/lists/' + str(list_id))
    tasklist = TaskList.objects.get(id=list_id)
    context = {
        'name': tasklist.name,
        'is_private': tasklist.is_private
    }
    return render(request, 'add_tasklist.html', context)


@login_required(login_url='/accounts/login')
def edit_task(request, task_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        tags = request.POST.getlist('tags')
        priority = request.POST['priority']
        list_id = request.POST['list_id']
        deadline = request.POST['deadline']
        dd = None
        if deadline != '':
            dd = datetime.strptime(deadline, '%m/%d/%Y %I:%M %p')
        try:
            task = Task.objects.get(id=task_id, created_user=request.user)
            task.title = title
            task.priority = priority
            task.description = description
            task.task_list = TaskList.objects.get(id=list_id)
            task.deadline = dd
            task.save()
            for tag in tags:
                task.tags.add(Tag.objects.get(id=int(tag)))
                task.save()
        except Exception as e:
            messages.error(request, 'ti ne admin')

        return redirect('/todolist')
    # print('---------', Task.objects.get(id=task_id).repeat_days)
    return render(request, 'edit.html', {'task': Task.objects.get(id=task_id)})


@login_required(login_url='/accounts/login')
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.period_val and task.period_val != 'N' and task.period_val != '':
        if task.period_val == 'D':
            task.deadline += relativedelta(days=+1)
        elif task.period_val == 'W':
            if task.repeat_days and len(task.repeat_days):
                today = datetime.now().weekday()
                days = [MO, TU, WE, TH, FR, SA, SU]
                new_week = True
                for day in task.repeat_days:
                    if int(day) - 1 > today:
                        new_week = False
                        task.deadline += relativedelta(weekday=days[day-1])
                if new_week:
                    first_day_number = int(task.repeat_days[0]) - 1
                    task.deadline += relativedelta(weekday=days[first_day_number])
            else:
                task.deadline += relativedelta(weeks=+1)
        elif task.period_val == 'M':
            task.deadline += relativedelta(months=+1)
        elif task.period_val == 'Y':
            task.deadline += relativedelta(years=+1)
    else:
        task.completed_user = request.user
        task.status = 'C'
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def trash_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'T'
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def delete_list(request, list_id):
    try:
        list = TaskList.objects.get(id=list_id, created_user=request.user)
        list.delete()
    except Exception as e:
        messages.warning(request, 'Ti ne admin')
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def repair_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'P'
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def completed(request):
    user = request.user
    tasks = Task.objects.filter(status='C')
    context = {
        'tasks': tasks,
    }
    return render(request, 'completed.html', context)


@login_required(login_url='/accounts/login')
def trash(request):
    user = request.user
    tasks = Task.objects.filter(status='T', created_user=user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'trash.html', context)


@login_required(login_url='/accounts/login')
def today(request):
    tasks = Task.objects.filter(status='P', deadline__lt=date.today() + timedelta(days=1))
    context = {
        'tasks': tasks,
    }
    return render(request, 'today.html', context)


@login_required(login_url='/accounts/login')
def next_week(request):
    tasks = Task.objects.filter(status='P', deadline__lt=date.today() + relativedelta(weeks=+1))
    context = {
        'tasks': tasks,
    }
    return render(request, 'today.html', context)


@login_required(login_url='/accounts/login')
def invite(request, list_id):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        try:
            tasklist = TaskList.objects.get(id=list_id, created_user=request.user)
            invited_user = User.objects.get(id=int(user_id))
            tasklist.users.add(invited_user)
            tasklist.save()
            list_tags = Tag.objects.filter(task_set__in=tasklist.task_set)
            for tag in list_tags:
                invited_user.tag_set.add(tag)
            invited_user.save()
        except Exception as e:
            messages.error(request, 'ti ne admin')
        return redirect('/todolist/lists/' + str(list_id))
    tasklist = TaskList.objects.get(id=list_id)
    context = {
        'users': User.objects.exclude(all_lists__in=[tasklist])
    }
    return render(request, 'invite.html', context)


@login_required(login_url='/accounts/login')
def kick(request, list_id, user_id):
    tasklist = TaskList.objects.get(id=list_id, created_user=request.user)
    kicked_user = User.objects.get(id=int(user_id))
    tasklist.users.remove(kicked_user)
    tasklist.save()
    return redirect('/todolist/lists/' + str(list_id))
