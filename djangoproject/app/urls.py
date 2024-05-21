from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainpage, name="mainpage"),
    path("login/", views.login_page, name="login"),
    path("singup/", views.signup, name="singup"),
    path('users/', views.user_list, name='user_list'),
    path('logout/', views.logout_view, name='logout'),
    path('list/<int:list_id>/', views.list_detail, name='list_detail'),
    path('task/<int:task_id>/', views.manage_task, name='manage_task'),
    path('list/<int:list_id>/delete/', views.delete_list, name='delete_list'),
]
