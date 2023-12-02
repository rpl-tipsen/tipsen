# urls.py
from django.urls import path
from .views import special_order

urlpatterns = [
    path('special_request/', special_order, name='special_order'),
    # Add more URL patterns as needed
]
