from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from .forms import SignUpForm,ExtendedAuthenticationForm
from .forms import SignUpForm, ExtendedAuthenticationForm, UserTaskForm
from django.contrib import messages
from django import forms
from .models import UserTask
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone


def mainpage(request):
    return render(request, 'main-page.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'users-admin.html', {'users': users})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('mainpage')
    else:
        form = SignUpForm()
    return render(request, 'sing-up.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = ExtendedAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_task_management')
    else:
        form = ExtendedAuthenticationForm()
    return render(request, 'log-in.html', {'form': form})

def user_task_management(request):
    if request.method == 'POST':
        if 'delete_task' in request.POST:
            task_id = request.POST.get('delete_task')
            task = get_object_or_404(UserTask, id=task_id, User=request.user)
            task.delete()
            return redirect('user_task_management')
        elif 'completed_task_id' in request.POST: 
            task_id = request.POST.get('completed_task_id')
            task = get_object_or_404(UserTask, id=task_id, User=request.user)
            task.completed = not task.completed
            if task.completed:
                task.completed_time = timezone.now()
            else:
                task.completed_time = None
            task.save()
            return redirect('user_task_management')
        elif 'edit_task' in request.POST:
            task_id = request.POST.get('edit_task')
            task = get_object_or_404(UserTask, id=task_id, User=request.user)
            form = UserTaskForm(request.POST, instance=task)
            
            form.save()
            return redirect('user_task_management')
        else:
            form = UserTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.User = request.user
                task.save()
                return redirect('user_task_management')
    else:
        form = UserTaskForm()

    filter_tag = request.GET.get('filter_tag')
    if filter_tag:
        user_tasks = UserTask.objects.filter(User=request.user, TaskTag__icontains=filter_tag)
    else:
        user_tasks = UserTask.objects.filter(User=request.user)

    return render(request, 'todo-list.html', {'form': form, 'user_tasks': user_tasks})