# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("", products, name="products"),
    path("<int:product_id>", product, name="product"),
    path("order/<int:product_id>", order_product,
         name="order_product"),
]
