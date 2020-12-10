from users.models import UserToken
from django.shortcuts import render, resolve_url
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import TaskForm
from .models import Task

from public import urls
from users import urls

from datetime import date
import uuid
import random as r

asks = [
    "¿Que nos toca hoy?",
    "¿Que hacemos?",
    "¡Asegurate de escribir una tarea super importante!"
]
asks_random_choice = r.randint(0, len(asks))
ask_len = asks_random_choice - 1

today = date.today()

# Create your views here.
def create_task_render(request):
    if not request.user.is_authenticated or request.session['token'] == None:
        return HttpResponseRedirect(reverse('home'))    
    return render(request, "tasks/create_task.html", {
        "task_form" : TaskForm(),
        "user_ask" : asks[ask_len],
        "status" : None
    })


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if request.POST['limit_date'] < date.strftime(today, "%Y-%m-%d"):
            return render(request, "tasks/create_task.html", {
                "task_form" : form,
                "user_ask" : asks[ask_len],
                "status" : False,
                "msg" : "La fecha limite no puede ser menor que la fecha actual" 
            })

        if form.is_valid():

            token = UserToken.objects.get(token=request.session['token'])

            task = Task(uuid.uuid4(), author_token=token, task=request.POST['task'], 
                        status=0, priority=request.POST['priority'], initial_date=today, 
                        limit_date=request.POST['limit_date'])
            task.save()

            return render(request, "tasks/create_task.html", {
                "task_form" : TaskForm(),
                "user_ask" : asks[ask_len],
                "status" : True,
                "msg" : "Tarea registrada"
            })
        
        else:
            return render(request, "tasks/create_task.html", {
                "task_form" : form,
                "user_ask" : asks[ask_len],
                "status" : False,
                "msg" : "No se pudo registrar la tarea. Datos invalidos"
            })
    else:
        return render(request, "tasks/create_task.html", {
            "task_form" : TaskForm(),
            "user_ask" : asks[ask_len],
            "status" : None,
        })

def list_all_user_tasks(request):
    token = UserToken.objects.get(token=request.session['token'])
    tasks = Task.objects.filter(author_token=token)
    return tasks

def get_all_tasks_count(request):
    token = UserToken.objects.get(token=request.session['token'])
    tasks_count = {
        "all" : Task.objects.filter(author_token=token).count(),
        "done" : Task.objects.filter(author_token=token, status=1).count(),
        "pending" : Task.objects.filter(author_token=token, status=0).count()
    }

    return tasks_count

def get_single_task(request, id):

    if not request.user.is_authenticated or request.session['token'] == None:
        return HttpResponseRedirect(reverse('login'))

    token = UserToken.objects.get(token=request.session['token'])
    task = Task.objects.get(id=id, author_token=token)
    
    days = int("".join([i for i in str(task.limit_date - task.initial_date).split(",")[0] if i.isdigit()])) 

    return render(request, "tasks/task.html", {
        "task_details" : task,
        "days_left" : days,
        "date_exceeded" : True if today > task.limit_date else False
    })

def update_status(request, id):
    token = UserToken.objects.get(token=request.session['token'])
    task = Task.objects.filter(id=id, author_token=token).update(status=1, accomplishment_date=today)    
    return HttpResponseRedirect(reverse('dashboard'))


def update_task_render(request, id):
    if not request.user.is_authenticated or request.session['token'] == None:
        return HttpResponseRedirect(reverse('home'))

    token = UserToken.objects.get(token=request.session['token'])
    task = Task.objects.get(id=id, author_token=token)

    form = TaskForm()
    form.initial = {
        "task" : task.task, 
        "priority" : task.priority, 
        "limit_date" : date.strftime(task.limit_date, "%Y-%m-%d")
    }

    return render(request, "tasks/update_task.html", {
        "task_form" : form,
        "user_ask" : "Actualice su tarea",
        "status" : None,
        "task_id" : task.id
    })

def update_task(request, id):

    token = UserToken.objects.get(token=request.session['token'])
    task = Task.objects.get(id=id, author_token=token)

    if request.POST['limit_date'] < date.strftime(today, "%Y-%m-%d"):

        form = TaskForm()
        form.initial = {
            "task" : task.task,
            "priority" : task.priority,
            "limit_date" : date.strftime(task.limit_date, "%Y-%m-%d")
        }

        return render(request, "tasks/update_task.html", {
            "task_form" : form,
            "user_ask" : "Actualice su tarea",
            "status" : False,
            "msg" : "La fecha limite no puede ser menor que la fecha actual",
            "task_id" : task.id             
        })
    
    task.task=request.POST['task']
    task.priority=request.POST['priority']
    task.limit_date=request.POST['limit_date']    
    task.save()
    
    return HttpResponseRedirect(reverse('dashboard'))

def delete_task(request, id):
    token = UserToken.objects.get(token=request.session['token'])
    task = Task.objects.filter(id=id, author_token=token).delete()
    return HttpResponseRedirect(reverse('dashboard'))

def delete_all_task(request):
    token = UserToken.objects.get(token=request.session['token'])
    task = Task.objects.filter(author_token=token).delete()
    return HttpResponseRedirect(reverse('dashboard'))