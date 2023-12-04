# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("payments", show_all_payments, name="show_all_payments"),
]