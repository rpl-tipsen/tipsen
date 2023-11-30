# urls.py
from django.urls import path
from .views import user_profile, create_address, update_address, delete_address

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("profile/address/create/", create_address, name="create_address"),
    path("profile/address/update/<int:address_id>", update_address, name="update_address"),
    path("profile/address/delete/<int:address_id>", delete_address, name="delete_address")
    # Add more URL patterns as needed
]
