from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Crea el usuario. Comprueba si el usuario existe
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate # Genera y elimina la cookie. Por ultimo está la autenticación de cuenta
from django.contrib.auth.decorators import login_required # Decorador que podemos colocar en cada función para "protegerla" y que tenga que estar loggeado para poder verlo
from django.db import IntegrityError # Error especifico
from .forms import TaskForm
from .models import Task
from django.utils import timezone
# Create your views here.


def home(request):
    return render(request, 'home.html', {})

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])  # crea el usurario
                user.save()
                login(request, user) # Con esto creado, podemos decir si las tareas son generadas por este usuario o, si tienen acceso a determinadas partes de la página, incluso mostrar su información
                return redirect('tasks')
            except IntegrityError: # Control de error especifico
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
                })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) # Solo muestra las tareas del usuario actual y las tarea que aún no está completo
    return render(request, "tasks.html", {'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # Solo muestra las tareas del usuario actual y las tarea que están completas
    return render(request, "tasks.html", {'tasks':tasks})

@login_required
def created_task(request):

    if request.method == 'GET':
        return render(request, 'created_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False) # Evita que se guarde dentro de la instancia de variable'commit=false'
            new_task.user = request.user # Session cookies de usuario
            new_task.save() # Genera un dato dentro de la bbdd
            return redirect('tasks')
        except ValueError:
            return render(request, 'created_task.html', {
            'form': TaskForm,
            'error': "Please provide valide data"
        })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user) # Éste método get object, realiza lo mismo que -> Task.objects.get, con la diferencia de que si dá error no tumba el servidor
        form = TaskForm(instance=task) # Llena el formulario con esa tarea
        return render(request, 'task_detail.html', {'task': task, 'form':form}) 
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user) # Añadiendo el user=request.user nos aseguramos de que solo pueda elegir tareas creadas por el usuario.
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form':form, 'error':"Error actualizando updating task"}) 

@login_required
def complete_task(request, task_id):
    task =get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task =get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.delete()
        return redirect('tasks')

@login_required
def signout(request): # Se llama así para no generar error (podría llamarse = cerrarSesion)
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
             })
        else:
            login(request, user)
            return redirect('tasks')