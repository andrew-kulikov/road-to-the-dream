from django.shortcuts import render, redirect

from .models import Task, TaskList, Tag


def index(request):
    #if request.user.is_anonymous:
    #    return redirect('/accounts/login')
    tasks = Task.objects.filter(user=request.user)
    task_lists = TaskList.objects.all()
    tags = Tag.objects.all()
    context = {
        'name': 'Andrew',
        'tasks': tasks,
        'task_lists': task_lists,
        'tags': tags
    }
    return render(request, 'index.html', context)


def details(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {
        'name': 'Andrew',
        'task': task
    }
    return render(request, 'details.html', context)


def list_details(request, list_id):
    list = TaskList.objects.get(id=list_id)
    tasks = list.task_set.all()
    context = {
        'name': 'Andrew',
        'tasks': tasks
    }
    return render(request, 'list_details.html', context)


def add(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        user = request.user
        task = Task(title=title, description=description, user=user)
        task.save()

        return redirect('/todolist')
    return render(request, 'add.html')
