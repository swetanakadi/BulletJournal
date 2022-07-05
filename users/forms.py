from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import TaskToDoList, TaskCheckList

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class TaskToDoListForm(ModelForm):
    class Meta:
        model = TaskToDoList
        fields = ['title', 'priority']


class TaskCheckListForm(ModelForm):
    class Meta:
        model = TaskCheckList
        fields = ['emotionalbeing', 'physicalbeing', 'gratitude']
