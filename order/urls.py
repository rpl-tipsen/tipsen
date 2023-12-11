# urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('special_request/', special_order, name='special_request'),
    path('verify/<str:order_id>', verify_paid_order, name='verify_paid_order'),
    path('reject/<str:order_id>', reject_unfully_paid_order, name='reject_unfully_paid_order'),
    path('admin/', manage_orders, name='manage_orders'),
    path('admin/update_status/<uuid:order_id>', update_order_status, name='update_order_status'),
    path('admin/add_description/<uuid:order_id>', add_order_description, name='add_order_description'),
    path('my_order/', show_my_order, name='my_order')
]