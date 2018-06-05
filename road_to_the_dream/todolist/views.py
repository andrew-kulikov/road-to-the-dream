from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Task


def index(request):
    tasks = Task.objects.all()[:10]
    context = {
        'name': 'Andrew',
        'tasks': tasks
    }
    return render(request, 'index.html', context)


def details(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {
        'name': 'Andrew',
        'task': task
    }
    return render(request, 'details.html', context)


def add(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']

        task = Task(title=title, description=description)
        task.save()

        return redirect('/todolist')
    return render(request, 'add.html')
