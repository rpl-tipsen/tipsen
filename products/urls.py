# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("", products, name="products"),
    path("<int:product_id>", product, name="product"),
    path("order/<int:product_id>", order_before_payment,
         name="order_before_payment"),
    path("order/<int:product_id>/<int:address_id>",
         order_after_payment, name="order_after_payment"),
]
