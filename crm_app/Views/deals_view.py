from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from crm_app.models import Customer, Deal
from crm_app.forms import DealForm


@login_required
def customer_deals_view(request):
    context = dict()
    request_user = request.user
    user = False
    if request.user:
        user = True
    form = DealForm(request.POST or None)
    if request.method == 'GET':
        form.fields['customer'].queryset = Customer.objects.filter(user=request_user)
        deals = Deal.objects.filter(customer__user=request_user).all()
        context['deals'] = deals

    if request.method == 'POST':
        if form.is_valid():
            deal = form.save()
            return redirect('crm:deals')

    context['form'] = form
    context['user'] = user
    return render(request, 'deals.html', context)


@login_required
def edit_deal_view(request, deal_id):
    context = dict()
    request_user = request.user
    deal = Deal.objects.filter(customer__user=request_user, id=deal_id).first()
    if deal is not None:
        if request.method == 'POST':
            form = DealForm(request.POST, instance=deal)
            if form.is_valid():
                form.save()
        else:
            form = DealForm(instance=deal)
            context['form'] = form
            return render(request, 'edit_deal.html', {'form': form})
    return redirect('crm:deals')
