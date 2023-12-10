from django.db import models
import uuid
from products.models import Product
from payment.models import Payment
from userprofile.models import Address
from authentication.models import AuthUser


class OrderStatus(models.Model):
    status = models.CharField(max_length=50)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_special_request = models.BooleanField(default=False)
    timestamp = models.TimeField(auto_now_add=True)
    status = models.ForeignKey(to=OrderStatus, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    description = models.TextField(max_length=150)
    ongkir = models.IntegerField(default=0)
    other_fee = models.IntegerField(default=0)
    subtotal = models.BigIntegerField()
    product = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING)
    payment = models.OneToOneField(to=Payment, on_delete=models.RESTRICT)
    address = models.ForeignKey(to=Address, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(to=AuthUser, on_delete=models.DO_NOTHING)


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
