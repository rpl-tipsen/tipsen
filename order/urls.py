# urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('special_request/', special_order, name='special_request'),
    path('verify/<int:order_id>', verify_paid_order, name='verify_paid_order'),
    path('reject/<int:order_id>', reject_unfully_paid_order, name='reject_unfully_paid_order'),
    path('admin/', manage_orders, name='manage_orders'),
    path('my_order/', show_my_order, name='my_order')
]
