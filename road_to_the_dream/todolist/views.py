from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import admin

from .models import Task, TaskList, Tag


def index(request):
    tasks = Task.objects.all()[:10]
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
