# urls.py
from django.urls import path
from .views import signup, login_view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    # Add more URL patterns as needed
]
