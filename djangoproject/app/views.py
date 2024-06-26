from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ExtendedAuthenticationForm, UserTaskForm, TaskListForm    
from .models import UserTask, TaskList
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import xml.etree.ElementTree as ET
from datetime import timedelta


def mainpage(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()
            return redirect('mainpage')  
    else:
        form = TaskListForm()

    if request.user.is_authenticated:
        user_lists = TaskList.objects.filter(user=request.user)
    else:
        user_lists = None

    return render(request, 'main-page.html', {'form': form, 'user_lists': user_lists})

def list_detail(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    if request.method == 'POST':
        form = UserTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.User = request.user
            task.TaskList = task_list
            task.save()
            return redirect('list_detail', list_id=list_id)
    else:
        form = UserTaskForm()

    filter_tag = request.GET.get('filter_tag')
    if filter_tag:
        user_tasks = UserTask.objects.filter(User=request.user, TaskList=task_list, TaskTag__icontains=filter_tag)
    else:
        user_tasks = UserTask.objects.filter(User=request.user, TaskList=task_list)
        
    now = timezone.now()
    for task in user_tasks:
        task.week = not task.completed and task.TaskCreateTime < now - timedelta(weeks=1)

    return render(request, 'todo-list.html', {'form': form, 'user_tasks': user_tasks, 'task_list': task_list})



def manage_task(request, task_id):
    task = get_object_or_404(UserTask, id=task_id, User=request.user)
    if request.method == 'POST':
        if 'delete_task' in request.POST:
            task.delete()
            return redirect('list_detail', list_id=task.TaskList.id)
        elif 'completed_task_id' in request.POST:
            task.completed = not task.completed
            if task.completed:
                task.completed_time = timezone.now()
                task.completed_note = request.POST.get('completed_note', '') 
            else:
                task.completed_time = None
                task.completed_note = None
            task.save()
            return redirect('list_detail', list_id=task.TaskList.id)
        elif 'edit_task' in request.POST:
            form = UserTaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('list_detail', list_id=task.TaskList.id)
    else:
        form = UserTaskForm(instance=task)

    return render(request, 'manage-task.html', {'form': form, 'task': task})



def delete_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    task_list.delete()
    return redirect('mainpage')

def rename_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    if request.method == 'POST':
        form = TaskListForm(request.POST, instance=task_list)
        if form.is_valid():
            form.save()
            return redirect('mainpage')
    else:
        form = TaskListForm(instance=task_list)
    
    return render(request, 'main-page.html', {'form': form, 'task_list': task_list})

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
                return redirect('mainpage')
    else:
        form = ExtendedAuthenticationForm()
    return render(request, 'log-in.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('mainpage')

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
                task.completed_note = request.POST.get('CompletedTaskNote', '') 
            else:
                task.completed_time = None
                task.completed_note = None
            task.save()
            return redirect('user_task_management')
        elif 'edit_task' in request.POST:
            task_id = request.POST.get('edit_task')
            task = get_object_or_404(UserTask, id=task_id, User=request.user)
            form = UserTaskForm(request.POST, instance=task)
            if form.is_valid():
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



def export_to_xml(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    user_tasks = UserTask.objects.filter(User=request.user, TaskList=task_list)

    x = ET.Element("Tasks")

    for task in user_tasks:
        taksElement = ET.SubElement(x, "Task")
        ET.SubElement(taksElement, "TaskName").text = task.TaskName
        ET.SubElement(taksElement, "TaskDescription").text = task.TaskDescription
        ET.SubElement(taksElement, "TaskTag").text = task.TaskTag
        ET.SubElement(taksElement, "TaskCreateTime").text = task.TaskCreateTime.isoformat()
        ET.SubElement(taksElement, "Completed").text = str(task.completed)
        if task.completed:
            ET.SubElement(taksElement, "CompletedTime").text = task.completed_time.isoformat() if task.completed_time else ''
            ET.SubElement(taksElement, "CompletedNote").text = task.completed_note if task.completed_note else ''

    xml_data = ET.tostring(x, encoding="utf-8")

    response = HttpResponse(xml_data, content_type="application/xml")
    response['Content-Disposition'] = f'attachment; filename="tasks_{list_id}.xml"'

    return response