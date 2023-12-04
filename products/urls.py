# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("", products, name="products"),
    path("<int:product_id>", product, name="product"),
    path("order/<int:product_id>", order_product, name="order_product"),
    path("admin", admin_products, name="admin-products"),
    path("admin/<int:product_id>", admin_product, name="admin-product"),
    path("admin/create", admin_create, name="admin-create"),
    path("admin/delete/<int:product_id>", admin_delete, name="admin-delete"),
]
