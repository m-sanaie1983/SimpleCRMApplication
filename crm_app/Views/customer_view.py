from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from crm_app.models import Customer, PhoneNumber
from crm_app.forms import CustomerForm, PhoneNumberFormSet, PhoneNumberForm
from django.forms import modelformset_factory, inlineformset_factory


@login_required
def customer_view(request):
    customer_form = CustomerForm()
    PhoneNumberFormSet = modelformset_factory(PhoneNumber, form=PhoneNumberForm, extra=1)
    customer_list = Customer.objects.filter(user=request.user).all()
    user = False
    if request.user:
        user = True
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        phone_number_formset = PhoneNumberFormSet(request.POST, queryset=PhoneNumber.objects.none())

        if customer_form.is_valid() and phone_number_formset.is_valid():
            customer = customer_form.save(commit=False)
            customer.user = request.user
            customer.save()

            for form in phone_number_formset:
                if form.cleaned_data:
                    phone_number = form.save(commit=False)
                    phone_number.customer = customer
                    phone_number.save()

            return redirect('crm:customers')

    else:
        phone_number_formset = PhoneNumberFormSet(queryset=PhoneNumber.objects.none())

    return render(request, 'customers.html', {
        'user': user,
        'customer_form': customer_form,
        'phone_number_formset': phone_number_formset,
        'customers': customer_list,
    })


@login_required
def edit_customer_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)

    user = False
    if request.user:
        user = True

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)
        phone_number_forms = PhoneNumberFormSet(request.POST, prefix='phone_numbers')

        if customer_form.is_valid() and phone_number_forms.is_valid():
            customer_form.save()
            existing_phone_numbers = list(customer.phone_numbers.all())
            for form in phone_number_forms:
                if form.cleaned_data:
                    phone_number = form.save(commit=False)
                    phone_number.customer = customer
                    phone_number.save()
                else:
                    if existing_phone_numbers:
                        phone_to_delete = existing_phone_numbers.pop(0)
                        phone_to_delete.delete()

            return redirect('customer_list')

    else:
        customer_form = CustomerForm(instance=customer)
        phone_number_forms = PhoneNumberFormSet(prefix='phone_numbers', queryset=customer.phone_numbers.all())

    return render(request, 'edit_customer.html', {
        'user': user,
        'customer_form': customer_form,
        'phone_number_formset': phone_number_forms,
    })


@login_required
def delete_customer_view(request, customer_id):
    if request.method == 'GET':
        user = request.user
        customer = get_object_or_404(Customer, id=customer_id, user=user)
        customer.delete()
        return redirect('crm:customers')
