from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, timedelta
from calendar import monthrange

from .models import TaskToDoList, TaskCheckList
from .forms import CreateUserForm, TaskToDoListForm, TaskCheckListForm

# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for "+ user)
            return redirect('login')
        else:
            messages.error(request, "Your form has errors. Please check and refill")
    context = { 'form' : form}
    return render(request, 'register.html', context=context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userpage')
        else:
            messages.info(request, "Username or password incorrect")

    return render(request, "login.html")


#This decorator will redirect to login page to the users who haven't logged in
@login_required(login_url='login')
def userPage(request):
    context = {'name': request.user }
    return render(request, 'userpage.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('login')

#This is working fine
def createTasks(request):
    form = TaskToDoListForm()
    if request.method == 'POST':
        form  = TaskToDoListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            priority = form.cleaned_data.get('priority')
            user = User.objects.get(username=request.user)
            if(title == '' or priority=='' ):
                return render(request, 'taskform.html')
            task = TaskToDoList(title=title, priority=priority, user_id=user.id)
            task.save()
            messages.success(request, 'Your task:'+ title + ' has been added successfully')
    form = TaskToDoListForm()
    context = {'form': form }
    return render(request, 'taskform.html', context=context)


#This is working fine
def createCheckList(request):
    form = TaskCheckListForm()
    if request.method == 'POST':
        form = TaskCheckListForm(request.POST)
        if form.is_valid():
            emotionalbeing = form.cleaned_data.get('emotionalbeing')
            physicalbeing = form.cleaned_data.get('physicalbeing')
            gratitude = form.cleaned_data.get('gratitude')
            user = User.objects.get(username=request.user)
            if emotionalbeing == '' and physicalbeing == '' and gratitude == '':
                messages.info(request, 'You have nothing in checklist to save for today')
                return redirect('userpage')
            else:
                try:
                    user_obj = TaskCheckList.objects.get(user_id=user.id, date=date.today())
                    user_obj.emotionalbeing= emotionalbeing
                    user_obj.physicalbeing= physicalbeing
                    user_obj.gratitude = gratitude
                    user_obj.save(update_fields=['emotionalbeing', 'physicalbeing', 'gratitude'])
                    messages.success(request, 'Your details have been updated for today')
                    return redirect('userpage')
                except TaskCheckList.DoesNotExist:
                    new_obj = TaskCheckList.objects.create(emotionalbeing=emotionalbeing, 
                    physicalbeing=physicalbeing, gratitude=gratitude, user_id=user.id)
                messages.success(request, 'Your details have been saved for today')
                return redirect('userpage')
    context = { 'form' : form }
    return render(request, 'checklistform.html', context=context)

'''
name-1 == task1 radiobutton
name-2 == task2 radiobutton
'''
def todayslist(request):
    user = User.objects.get(username=request.user)
    req_date = date.today()
    tasks = TaskToDoList.objects.filter(user_id=user.id, date=req_date)
    records = []
    updated_records = []
    c_records = []
    if request.method == 'POST':
        updatedEmotionalBeing = request.POST.get('updatedEmotionalBeing')
        updatedPhysicalBeing = request.POST.get('updatedPhysicalBeing')
        updatedGratitude = request.POST.get('updatedGratitude')
        i=1
        radio = "name-"
        for task in tasks:
            button = radio + str(i)
            i+=1
            value = request.POST.get(button)
            #print(value)
            new_rec = TaskToDoList.objects.get(title=task.title, date=date.today())
            if value == 'MIG':
                #i.e if task is migrated then change its date to tomorrrow and set status to pending
                new_rec.status = 'PEN'
                new_rec.date = date.today() + timedelta(days=1)
                print(new_rec.date)
                new_rec.save(update_fields=['status', 'date'])
            else:
                new_rec.status = value
                new_rec.save(update_fields=['status'])

        if (updatedEmotionalBeing is not None and updatedPhysicalBeing is not None and 
        updatedGratitude is not None):
            updatedEmotionalBeing.strip()
            updatedPhysicalBeing.strip()
            updatedGratitude.strip()
            TaskCheckList.objects.filter(user_id=user.id, date=req_date).update(emotionalbeing=updatedEmotionalBeing,
            physicalbeing=updatedPhysicalBeing, gratitude=updatedGratitude) 
            messages.info(request, "Your details have been updated")
        return redirect('userpage')
    else:
        for task in tasks:
            rec = { 'title': task.title, 'status': task.status, 'priority': task.priority }
            records.append(rec)
        checklists = TaskCheckList.objects.filter(user_id=user.id, date=req_date)    
        for clist in checklists:
            rec = {'emotionalbeing': clist.emotionalbeing,
                    'physicalbeing' : clist.physicalbeing,
                    'gratitude' : clist.gratitude 
                }
            c_records.append(rec)
    context = {'records': records, 'c_records': c_records }
    return render(request, 'todayslist.html', context=context)

def weeks_report(request):
    #visualization of last 7 day's productivity and well being 
    req_date = date.today() - timedelta(days=6)
    current_user = User.objects.get(username=request.user)
    output_todo_dict = {}    
    total_tasks = 0
    date_str = ''
    for i in range(7):
        completed_tasks = 0
        cancelled_tasks = 0
        days_record = TaskToDoList.objects.raw('''select * from users_tasktodolist where user_id=%s 
        and date=%s''', params=[current_user.id, req_date])
        total_tasks = len(days_record)
        date_str = req_date.strftime("%d %b %Y %A")
        for j in range(total_tasks):
            task = days_record[j]
            if task.status == 'COM':
                completed_tasks+=1
            if task.status == 'CAN':
                cancelled_tasks += 1
        if (total_tasks - cancelled_tasks != 0):
            percent_work_done = ( completed_tasks * 100 )/ (total_tasks - cancelled_tasks)
            output_todo_dict[date_str] = percent_work_done
        else:
            output_todo_dict[date_str] = 'You had no tasks'

        req_date = req_date + timedelta(days=1)
    #Till here data is collected from ToDoList table
    #print(output_todo_dict)
    req_date = date.today() - timedelta(days=6)
    checklist_records = TaskCheckList.objects.filter(user_id=current_user.id, 
    date__range=(req_date, date.today()))
    output_checklist_dict = {}
    for record in checklist_records:
        date_str = record.date.strftime("%d %b %Y %A")
        output_checklist_dict[date_str] = [ record.emotionalbeing,
        record.physicalbeing, record.gratitude ]
    #print(output_todo_dict, output_checklist_dict)
    return render(request, 'weeks_report.html', context={'output_todo_dict': output_todo_dict,
    'output_checklist_dict' : output_checklist_dict} )


def months_report(request):
    #visualization of previous month's productivity
    now = date.today()
    req_date = date(now.year, now.month, 1)
    print(now.year, now.month, req_date)
    current_user = User.objects.get(username=request.user)
    total_tasks = 0
    date_str = ''
    no_of_days = monthrange(now.year, now.month)[1]
    output_todo_dict = {}
    for i in range(no_of_days):
        if req_date > date.today(): 
            break                   #No need of future data
        completed_tasks = 0
        cancelled_tasks = 0
        days_record = TaskToDoList.objects.raw('''select * from users_tasktodolist where user_id=%s 
        and date=%s''', params=[current_user.id, req_date])
        total_tasks = len(days_record)
        date_str = req_date.strftime("%d %b %Y %A")
        for j in range(total_tasks):
            task = days_record[j]
            if task.status == 'COM':
                completed_tasks+=1
            if task.status == 'CAN':
                cancelled_tasks += 1
        if (total_tasks - cancelled_tasks != 0):
            percent_work_done = ( completed_tasks * 100 )/ (total_tasks - cancelled_tasks)
            output_todo_dict[date_str] = percent_work_done
        else:
            output_todo_dict[date_str] = 'You had no tasks'

        req_date = req_date + timedelta(days=1)

    return render(request, 'month_report.html', context={'output_todo_dict': output_todo_dict})