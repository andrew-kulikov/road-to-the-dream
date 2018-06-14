from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, TaskList, Tag
from datetime import datetime


@login_required(login_url='/accounts/login')
def index(request):
    tasks = Task.objects.filter(user=request.user, status='P')
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
    context = {
        'task': task
    }
    return render(request, 'details.html', context)


@login_required(login_url='/accounts/login')
def list_details(request, list_id):
    list = TaskList.objects.get(id=list_id)
    tasks = list.task_set.all()
    users = list.users.all()
    context = {
        'tasks': tasks,
        'users': users
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
        print(request.POST)
        deadline = request.POST['deadline']
        dd = datetime.strptime(deadline, '%m/%d/%Y %I:%M %p')
        user = request.user
        task = Task(title=title, description=description, user=user, priority=priority, deadline=dd)
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
        tasklist = TaskList(name=name, is_private=is_private)
        tasklist.save()
        tasklist.users.add(user)
        tasklist.save()

        return redirect('/todolist')
    return render(request, 'add_tasklist.html')


@login_required(login_url='/accounts/login')
def edit_task(request, task_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        tags = request.POST.getlist('tags')
        priority = request.POST['priority']
        user = request.user
        task = Task.objects.get(id=task_id)
        task.title = title
        task.user = user
        task.priority = priority
        task.description = description
        task.save()
        for tag in tags:
            task.tags.add(Tag.objects.get(id=int(tag)))
            task.save()

        return redirect('/todolist')
    return render(request, 'edit.html')


@login_required(login_url='/accounts/login')
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
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
def repair_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'P'
    task.save()
    return redirect('/todolist')


@login_required(login_url='/accounts/login')
def completed(request):
    user = request.user
    tasks = Task.objects.filter(status='C', user=user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'completed.html', context)


@login_required(login_url='/accounts/login')
def trash(request):
    user = request.user
    tasks = Task.objects.filter(status='T', user=user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'trash.html', context)
