from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User, Group
from . import roles
from .decorators import admin_required, member_required


def index_view(request):
    roles.create_groups()
    return render(request, 'index.html')


@member_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            member_group = Group.objects.filter(name='Members').first()
            user.groups.add(member_group.id)
            login(request, user)
            return redirect('crm:dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate user if exist
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('crm:dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
