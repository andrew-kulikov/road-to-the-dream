from django.contrib.auth import login
from django.shortcuts import render, redirect
from .user_create_form import UserCreateForm
from .login_form import LoginForm
from django.contrib.auth.views import logout
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/todolist')
    else:
        form = UserCreateForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/todolist')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(request.GET.get('next'))
