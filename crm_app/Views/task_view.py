from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from crm_app.models import Customer, Deal, Task
from crm_app.forms import DealForm, TaskForm


@login_required
def tasks_view(request):
    context = dict()
    request_user = request.user
    user = False
    if request.user:
        user = True
    form = TaskForm(request.POST or None)
    if request.method == 'GET':
        form.fields['customer'].queryset = Customer.objects.filter(user=request_user).all()
        form.fields['deal'].queryset = Deal.objects.filter(customer__user=request_user).all()
        tasks = Task.objects.filter(Q(customer__user=request_user) | Q(deal__customer__user=request_user)).all()
        context['tasks'] = tasks

    if request.method == 'POST':
        if form.is_valid():
            deal = form.save()
            return redirect('crm:tasks')

    context['form'] = form
    context['user'] = user
    return render(request, 'tasks.html', context)


@login_required
def edit_task_view(request, task_id):
    context = dict()
    request_user = request.user
    task = Task.objects.filter(
        Q(customer__user=request_user) | Q(deal__customer__user=request_user) & Q(id=task_id)).first()
    if task is not None:
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                user_group = request_user.groups.first()
                group = user_group.name
                status_value = form.cleaned_data['status']
                if status_value == 'Done' and group != 'Admins':
                    return redirect('crm:tasks')
                form.save()
        else:
            form = TaskForm(instance=task)
            context['form'] = form
            return render(request, 'edit_task.html', {'form': form})
    return redirect('crm:tasks')
