from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from crm_app.forms import SignupForm, LoginForm
from django.contrib.auth.models import User, Group
from crm_app import roles
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from crm_app.models import Deal, Customer, Task


def index_view(request):
    roles.create_groups()
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    context = dict()
    # I put user false or true in context to show logout button enable if user loged in
    user = False
    request_user = request.user
    if request_user:
        user = True

    # get data counts for dashboard
    deals = Deal.objects.filter(customer__user=request_user).all().count()
    tasks = Task.objects.filter(Q(customer__user=request_user) | Q(deal__customer__user=request_user)).all().count()
    customers = Customer.objects.filter(user=request_user).all().count()
    context['user'] = user
    context['deals'] = deals
    context['tasks'] = tasks
    context['customers'] = customers

    return render(request, 'dashboard.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            member_group = Group.objects.filter(name=role).first()
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
