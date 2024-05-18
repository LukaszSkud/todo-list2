from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import mainpage

urlpatterns = [
    path("", views.mainpage, name="mainpage"),
    path("login/", views.login_page, name="login"),
    path("singup/", views.signup, name="singup"),
    path('users/', views.user_list, name='user_list'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mainpage'), name='logout'),
    path('user/todo-list/', views.user_task_management, name='user_task_management'),



]

