from django.urls import path, include
from .Views import general_views, customer_view

app_name = "crm"
urlpatterns = [
    path('dashboard', general_views.dashboard_view, name='dashboard'),
    path('customers', customer_view.customer_view, name='customers'),
    path('edit_customer/<int:customer_id>/', customer_view.edit_customer_view, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', customer_view.delete_customer_view, name='delete_customer'),
]
