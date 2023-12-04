from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from order.models import Order
from .models import Payment


@login_required
def show_all_payments(request):
    user = request.user
    if not user.is_admin:
        return redirect("home")
    
    orders = Order.objects.filter(status="Menunggu Verifikasi Pembayaran")
    if len(orders) == 0:
        return render(request, "", {"error": "Belum ada order"})
    payments = [order.payment for order in orders]

    return render(request, "", {"orders": orders, "payments": payments})

