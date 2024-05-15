from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from .forms import SignUpForm,ExtendedAuthenticationForm
from django.contrib import messages


def mainpage(request):
    return render(request,'main-page.html')

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
                messages.success(request, "Zalogowano pomyślnie")
                return redirect('/')
            else:
                form.add_error(None, 'Nieprawidłowy adres email lub hasło.')
    else:
        form = ExtendedAuthenticationForm()
    return render(request, 'log-in.html', {'form': form})
