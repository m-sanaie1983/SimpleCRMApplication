from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name}"


class PhoneNumber(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='phone_numbers')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.phone_number


class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=100)
    closing_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer.name}'s Deal - ${self.value}"


class Task(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Canceled', 'Canceled'),
        ('Done', 'Done'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
