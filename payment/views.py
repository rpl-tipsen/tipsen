from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from order.models import Order, OrderStatus
from .models import Payment



@login_required
def show_unverified_payments(request):
    user = request.user
    if not user.is_admin:
        return redirect("home")
    

    order_status = OrderStatus.objects.get(status='Menunggu Verifikasi')
    orders = Order.objects.filter(status=order_status) 

  
    payments = [order.payment for order in orders]

    return render(request, "payments/verify_payments.html", {"orders": orders, "payments": payments})

