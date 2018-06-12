from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, TaskList, Tag


@login_required(login_url='/accounts/login')
def index(request):
    tasks = Task.objects.filter(user=request.user)
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
        user = request.user
        task = Task(title=title, description=description, user=user)
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
