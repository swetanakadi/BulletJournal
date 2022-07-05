from django.contrib import admin
from .models import TaskToDoList, TaskCheckList
# Register your models here.

admin.site.register(TaskToDoList)
admin.site.register(TaskCheckList)