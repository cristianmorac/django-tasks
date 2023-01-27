from django.shortcuts import render, redirect
from django.http import HttpResponse

# formulario de autenticación y registro
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# registrar usuarios
from django.contrib.auth.models import User

# crear la cookie de logueo y realizar deslogueo
from django.contrib.auth import login, logout, authenticate

# Error en la base de datos
from django.db import IntegrityError

# manejo de errores
from django.shortcuts import get_object_or_404

# formulario
from .forms import TaskForm

# importar el modelo
from .models import Task

# fecha
from django.utils import timezone

# decoradores de logueo
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    task = Task.objects.all()
    return render(request,'home.html/',{
        'task':task
    })

def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
    else:
        # comparar contraseñas
        if request.POST['password1'] == request.POST['password2']:
            # manejo de errores try:except
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                # guardar el usuario
                user.save()
                # crear sesión id
                login(request,user)
                # redireccionar a otra pagina
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{
                # mostrar formulario django
                'form': UserCreationForm,
                # enviar error
                'error': 'Username already exists'
                })

        return render(request,'signup.html/',{
            # mostrar formulario django
            'form': UserCreationForm,
            # enviar error
            'error': 'Password do not match'
            })
    # mostrar pagina signup  
    return render(request,'signup.html/',{
        # mostrar formulario django
        'form': UserCreationForm
    })

@login_required
def tasks(request):
    # filtras por usuario e incompletas
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    # filtras por usuario e incompletas
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks.html', {
        'tasks': tasks
    })

@login_required
def task_detail(request,task_id):
    print(task_id)

    if request.method == 'GET':

        # Obtener un dato: Task:modelo pk:id
        task = get_object_or_404(Task,pk=task_id) 
        # mostrar contenido en formulario
        form = TaskForm(instance=task)
        return render(request,'task_detail.html', {
            'task': task,
            'form': form,
        })
    else:
        try:
            # actualizar tarea
            print(request.POST)
            #pk:id user:mismo usuario
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'Error updating task'
        })

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        print(task.datecompleted)
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        # eliminar tarea
        task.delete()
        return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):

    if request.method == 'GET':
        return render(request,'signin.html',{
        'form': AuthenticationForm
        })
    else:
        # validar los parametros que envia
        print(request.POST)
        # validar las credenciales
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        # usuario no valido retorna error
        if user is None:
            return render(request,'signin.html',{
            'form': AuthenticationForm,
            'error': 'is username or password is incorrect'
            })
        # usuario valido retorna su sesión y redirecciona a task
        else:
            login(request,user)
            return redirect('tasks')

@login_required
def create_task(request):

    if request.method == 'GET':  
        return render(request,'create_task.html', {
            'form': TaskForm,
        })
    else:
        try:
            print(request.POST)
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valida data'
        })