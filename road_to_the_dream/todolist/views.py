from datetime import datetime, date, timedelta

from dateutil.relativedelta import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponseBadRequest

from . import parsers
from .models import Task, TaskList, Tag, SubTask


@login_required(login_url='/accounts/login')
def index(request):
    sort_type = None
    if 'sort_type' in request.GET:
        sort_type = request.GET['sort_type']
    parsers.check_overdue()
    tasks = Task.objects.filter(Q(created_user=request.user) & Q(status='P') | Q(status='O'))
    if sort_type:
        tasks = tasks.order_by(sort_type)
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
    task = get_object_or_404(Task, id=task_id)
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
        'pending_st': task.subtask_set.filter(status='P'),
        'completed_st': task.subtask_set.filter(status='C'),
    }
    return render(request, 'details.html', context)


@login_required(login_url='/accounts/login')
def list_details(request, list_id):
    list = get_object_or_404(TaskList, id=list_id)
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
        priority = int(request.POST['priority'])
        list_id = request.POST['list_id']
        deadline = request.POST['deadline']
        period = request.POST['period']
        days = request.POST.getlist('days')
        count = request.POST['count']
        dd = None
        if deadline != '':
            dd = datetime.strptime(deadline, settings.DATETIME_PATTERN)
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
            task.period_count = int(count)
            if period == 'W':
                task.repeat_days = days
        task.save()
        task.tags.clear()
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
            tasklist = get_object_or_404(TaskList, id=list_id, created_user=user)
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
    tasklist = get_object_or_404(TaskList, id=list_id)
    context = {
        'name': tasklist.name,
        'is_private': tasklist.is_private
    }
    return render(request, 'add_tasklist.html', context)


@login_required(login_url='/accounts/login')
def edit_task(request, task_id):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            description = request.POST['description']
            tags = request.POST.getlist('tags')
            priority = int(request.POST['priority'])
            list_id = request.POST['list_id']
            deadline = request.POST['deadline']
            period = request.POST['period']
            days = request.POST.getlist('days')
            count = request.POST['count']
            dd = None
            if deadline != '':
                dd = datetime.strptime(deadline, settings.DATETIME_PATTERN)
        except (KeyError, ValueError, AttributeError):
            return HttpResponseBadRequest()
        try:
            task = Task.objects.get(id=task_id, created_user=request.user)
            print(task)
            task.title = title
            task.priority = priority
            task.description = description
            # ??
            task.task_list = TaskList.objects.get(id=list_id)
            task.deadline = dd
            task.save()
            if dd:
                task.period_val = period
                task.period_count = int(count)
                if period == 'W':
                    task.repeat_days = days
            task.save()
            task.tags.clear()
            for tag in tags:
                task.tags.add(Tag.objects.get(id=int(tag)))
            task.save()
        except TaskList.DoesNotExist:
            return HttpResponseBadRequest()
        except Task.DoesNotExist:
            messages.error(request, "You don't have permission to edit this task")

        return redirect('/todolist')
    task = get_object_or_404(Task, id=task_id, task_list__in=request.user.all_lists.all())
    context = {
        'task': task,
        'selected_tags': task.tags.all(),
        'deadline': datetime.strftime(task.deadline, settings.DATETIME_PATTERN),
        'selected_days': task.repeat_days
    }
    return render(request, 'edit.html', context)


@login_required(login_url='/accounts/login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, task_list__in=request.user.all_lists.all())
    task = parsers.complete_task(task, request.user)
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def trash_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_user=request.user)
    task.status = 'T'
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_user=request.user)
    task.delete()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def delete_list(request, list_id):
    try:
        list = get_object_or_404(TaskList, id=list_id, created_user=request.user)
        list.delete()
    except Exception as e:
        messages.warning(request, 'Ti ne admin')
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def repair_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_user=request.user)
    for st in task.subtask_set.all():
        st.status = 'P'
    task.status = 'P'
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def completed(request):
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
        try:
            user_id = request.POST['user_id']
            tasklist = TaskList.objects.get(id=list_id, created_user=request.user)
            invited_user = User.objects.get(id=int(user_id))
            tasklist.users.add(invited_user)
            tasklist.save()
            list_tags = Tag.objects.filter(task_set__in=tasklist.task_set)
            for tag in list_tags:
                invited_user.tag_set.add(tag)
            invited_user.save()
        except KeyError as e:
            return HttpResponseBadRequest()
            # messages.error(request, 'ti ne admin')

        return redirect('/todolist/lists/' + str(list_id))
    tasklist = get_object_or_404(TaskList, id=list_id)
    context = {
        'users': User.objects.exclude(all_lists__in=[tasklist])
    }
    return render(request, 'invite.html', context)


@login_required(login_url='/accounts/login')
def kick(request, list_id, user_id):
    tasklist = get_object_or_404(TaskList, id=list_id, created_user=request.user)
    kicked_user = User.objects.get(id=int(user_id))
    tasklist.users.remove(kicked_user)
    tasklist.save()
    return redirect('/todolist/lists/' + str(list_id))


@login_required(login_url='/accounts/login')
def complete_subtask(request, subtask_id):
    # 404?
    st = get_object_or_404(SubTask, id=subtask_id)
    st.status = 'C'
    st.save()
    task = st.task
    if task.subtask_set.count() == task.subtask_set.filter(status='C').count():
        complete_task(request, task.id)
    return redirect('/todolist/details/' + str(st.task_id))


@login_required(login_url='/accounts/login')
def delete_subtask(request, subtask_id):
    print(request.user.all_lists.all())
    st = get_object_or_404(SubTask, id=subtask_id, task__task_list__in=request.user.all_lists.all())
    st.delete()
    return redirect('/todolist/details/' + str(st.task_id))


@login_required(login_url='/accounts/login')
def repair_subtask(request, subtask_id):
    st = get_object_or_404(SubTask, id=subtask_id, task__in=Task.objects.filter(task_list__in=request.user.all_lists.all()))
    st.status = 'P'
    st.save()
    task = st.task
    task.status = 'P'
    task.completed_user = None
    task.save()
    return redirect('/todolist/details/' + str(st.task_id))
