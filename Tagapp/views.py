from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from .forms import CreateUserForm


def home(request):
    return render(request, 'tagapp/home.html')


def signup_user(request):
    form = CreateUserForm()

    if request.method == 'GET':
        return render(request, 'tagapp/signupuser.html', {'form': form})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('search')
            except IntegrityError:
                return render(request, 'tagapp/signupuser.html',
                              {'form': form, 'error': "This username is already taken! Please choose a new username."})
        else:
            # Tell the user that password didn't match
            return render(request, 'tagapp/signupuser.html',
                          {'form': form, 'error': "Passwords do not match!"})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'tagapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'tagapp/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('search')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def search(request):
    return render(request, 'tagapp/search.html')
