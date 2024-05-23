from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainpage, name="mainpage"),
    path("login/", views.login_page, name="login"),
    path("singup/", views.signup, name="singup"),
    path('logout/', views.logout_view, name='logout'),
    path('list/<int:list_id>/', views.list_detail, name='list_detail'),
    path('task/<int:task_id>/', views.manage_task, name='manage_task'),
    path('list/<int:list_id>/delete/', views.delete_list, name='delete_list'),
    path('user_task_management/', views.user_task_management, name='user_task_management'),
    path('list/<int:list_id>/rename/', views.rename_list, name='rename_list'),
    path('export-tasks/<int:list_id>/', views.export_to_xml, name='export_to_xml'),


]
