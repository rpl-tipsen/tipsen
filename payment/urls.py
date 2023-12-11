# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("payments", show_unverified_payments, name="show_unverified_payments"),
]