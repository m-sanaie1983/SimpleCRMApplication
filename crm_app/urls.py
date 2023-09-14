from django.urls import path, include
from .Views import general_views, customer_view,deals_view

app_name = "crm"
urlpatterns = [
    path('dashboard', general_views.dashboard_view, name='dashboard'),
    path('customers', customer_view.customer_view, name='customers'),
    path('edit_customer/<int:customer_id>/', customer_view.edit_customer_view, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', customer_view.delete_customer_view, name='delete_customer'),
    path('deals', deals_view.customer_deals_view, name='deals'),
    path('edit_deal/<int:deal_id>/', deals_view.edit_deal_view, name='edit_deal'),
]
