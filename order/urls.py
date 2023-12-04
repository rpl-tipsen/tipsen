# urls.py
from django.urls import path
from .views import special_order, manage_orders

urlpatterns = [
    path('special_request/', special_order, name='special_order'),
    path('admin/', manage_orders, name='manage_orders')
]
