from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, FileForm
from .models import Todo, File
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .utils import find_file


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Username has already been taken'})

        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm, 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required()
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required()
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            if request.POST.get('file'):
                print(newtodo.pk)
                return redirect('todo_file', newtodo.pk)
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again'})


def todo_file(request, todo_pk):
    todo = Todo.objects.get(pk=todo_pk)
    if todo and request.method == 'GET':
        if find_file(todo) and request.user.username == todo.user.username:
            return redirect('currenttodos')
        elif find_file(todo) and request.user.username != todo.user.username:
            return redirect('currenttodos')
        elif request.user.username != todo.user.username:
            return redirect('currenttodos')
        else:
            return render(request, 'todo/upload_file.html')
    else:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.save()
            todo.file = new_file
            todo.save()
            return redirect('currenttodos')
        print(form)
@login_required()
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, Datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required()
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        if find_file(todo.Title):
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'file': todo.file.file})
        else:
            form = TodoForm(instance=todo)
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html',
                          {'todo': todo, 'form': form, 'error': 'Bad data passed in. Try again'})


@login_required()
def viewcompletedtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        if find_file(todo.Title):
            return render(request, 'todo/viewcompletedtodo.html', {'todo': todo, 'file': todo.file.file})
        else:
            form = TodoForm(instance=todo)
            return render(request, 'todo/viewcompletedtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewcompletedtodo.html',
                          {'todo': todo, 'form': form, 'error': 'Bad data passed in. Try again'})


@login_required()
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.Datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required()
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, Datecompleted__isnull=False).order_by('-Datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required()
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
