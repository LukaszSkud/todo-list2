from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserTask

class SignUpForm(forms.Form):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
class ExtendedAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        
class UserTaskForm(forms.ModelForm):
    class Meta:
        model = UserTask
        fields = ['TaskName', 'TaskDescription']
