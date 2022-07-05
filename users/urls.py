from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.registerPage, name = 'register'),
    path('login', views.loginPage, name = 'login'),
    path('userpage', views.userPage, name = 'userpage'),
    path('logout', views.logoutUser, name = 'logout'),
    path('createTasks', views.createTasks, name = 'createTasks'),
    path('createCheckList', views.createCheckList, name = 'createCheckList'),
    path('todayslist', views.todayslist, name = 'todayslist'),
    path('weeks_report', views.weeks_report, name = 'weeks_report'),
    path('months_report', views.months_report, name = 'months_report'),
      
]