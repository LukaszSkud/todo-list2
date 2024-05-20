from django.db import models
from django.contrib.auth.models import User
from django import forms

class UserTask(models.Model):
    id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    TaskName = models.CharField(max_length=50)
    TaskDescription = models.CharField(max_length=500)
    TaskTag = models.CharField(max_length=50, default="None")
    TaskCreateTime = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_time = models.DateTimeField(null=True, blank=True)
    
    
