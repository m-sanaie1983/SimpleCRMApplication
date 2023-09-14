from django import forms
from django.forms import modelformset_factory

from .models import Customer, PhoneNumber, Deal, Task


class SignupForm(forms.Form):
    role_choices = [
        ('Admins', 'Admin'),
        ('Managers', 'Manager'),
        ('Salereps', 'Sale Representative'),
    ]
    role = forms.ChoiceField(choices=role_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


PhoneNumberFormSet = modelformset_factory(
    PhoneNumber,
    form=PhoneNumberForm,
    extra=1,
)


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['customer', 'value', 'stage', 'closing_date', 'status']

        widgets = {
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'customer', 'deal']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
