from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from order.models import Order
from .models import Payment


@login_required
def show_all_payments(request):
    orders = Order.objects.filter(status="Menunggu Verifikasi Pembayaran")
    payments = [order.payment for order in orders]

    return render(request, "", {"orders": orders, "payments": payments})

