from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class TaskToDoList(models.Model):
    status_choices = [
        ('COM', 'COMPLETED'),
        ('PEN', 'PENDING'),
        ('MIG', 'MIGRATED'),
        ('CAN', 'CANCELLED'),
    ]

    priority_choices = [
        ('I', 'IMPORTANT'),
        ('U', 'URGENT'),
        ('C', 'CASUAL')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    priority = models.CharField(max_length=1, choices=priority_choices)
    status = models.CharField(max_length=3, choices=status_choices, default='PEN')
    date = models.DateField(default=date.today, editable=True)

    def __str__(self):
        return self.title + ' ' + self.date.strftime("%d %b %Y")

class TaskCheckList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emotionalbeing = models.TextField(null=True, blank=True)
    physicalbeing = models.TextField(null=True, blank=True)
    gratitude = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return self.date.strftime("%d %b %Y %A")