from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from .models import Order, OrderStatus
from payment.models import Payment
from products.models import Product
from .forms import ImageForm
from io import BufferedReader
import supabase
import mimetypes
import uuid
from tipsen.settings import SUPABASE

# Create your views here.

BUCKET_NAME = "payment"

sb = supabase.create_client(supabase_url=SUPABASE["url"], supabase_key=SUPABASE["key"])


@login_required
def verify_paid_order(request, order_id):
    user = request.user
    if not user.is_admin:
        return redirect("home")

    order = Order.objects.filter(id=order_id)
    if not order:
        return render(request, "payments/verify_payments.html", context={"error": f"Order dengan id {order_id} tidak ditemukan"})
    order.update(status = "Pembayaran Terverifikasi")

    return redirect("show_unverified_payments")


@login_required
def reject_unfully_paid_order(request, order_id):
    user = request.user
    if not user.is_admin:
        return redirect("home")
    
    order = Order.objects.filter(id=order_id)
    if not order:
        return render(request, "payments/verify_payments.html", context={"error": f"Order dengan id {order_id} tidak ditemukan"})
    order.delete()

    return redirect("show_unverified_payments")


@login_required
def special_order(request):
    addresses = Address.objects.filter(user=request.user._wrapped)
    banks = ["BCA", "Mandiri", "BNI"]

    if request.method == "POST":
        product = Product.objects.get(id=3)
        address = Address.objects.get(user=request.user._wrapped, id=int(request.POST.get("address")))
        status = OrderStatus.objects.get(status="Menunggu Verifikasi")
        payment = handle_payment_creation(request=request)
        Order.objects.create(
            is_special_request=True,
            status=status,
            quantity=1,
            description=f"{request.POST['product_link']}\n\n{request.POST['description']}",
            ongkir=10000,
            subtotal=int(request.POST["amount_paid"]),
            product=product,
            user=request.user._wrapped,
            payment=payment,
            address=address,
        ).save()
        return render(
            request=request,
            template_name="order/special_order.html",
            context={"addresses": addresses, "banks": banks, "success": True},
        )
    return render(
        request=request, template_name="order/special_order.html", context={"addresses": addresses, "banks": banks}
    )


@login_required
def show_my_order(request):
    orders = Order.objects.filter(user=request.user._wrapped)

    return render(request=request, template_name="order/my_order.html", context={'orders' : orders})


def handle_payment_creation(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.cleaned_data["image"]

        # Initialize Supabase client

        # Read the image file into memory
        image_data = BufferedReader(image.file)
        random_filename = str(uuid.uuid4()) + "_" + image.name

        content_type, encoding = mimetypes.guess_type(image.name)
        file_options = {"content-type": content_type} if content_type else {}

        # Upload the image to Supabase Bucket Storage
        response = sb.storage.from_(BUCKET_NAME).upload(
            path=random_filename, file=image_data, file_options=file_options
        )
        if response.status_code == 201 or response.status_code == 200:
            image_link = f"{SUPABASE['url']}/storage/v1/object/public/{BUCKET_NAME}/{random_filename}"
        else:
            return "Failed to create payment"

        payment = Payment.objects.create(
            payment_reference_number="ABC6969",
            jumlah=request.POST["amount_paid"],
            bank=request.POST["bank"],
            image_link=image_link,
        )

        payment.save()
        return payment


@login_required
def manage_orders(request):
    if not request.user.is_admin:
        return redirect("home")

    orders = Order.objects.all().order_by("id")

    if request.method == "POST":
        query = request.POST.get("query")
        order = Order.objects.get(id=request.POST.get("order_id"))

        if order:
            if query == "update-status":
                status = request.POST.get("status")
                order.status = status
                order.save()
            elif query == "add-desc":
                description = request.POST.get("description")
                order.description = description
                order.save()

    return render(request=request, template_name="order/manage_orders.html", context={"orders": orders})
