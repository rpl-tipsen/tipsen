from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from payment.models import Payment
from .models import Product
from .forms import *
from order.models import Order
from userprofile.models import Address
from order.forms import ImageForm
from io import BufferedReader
import supabase
import mimetypes
import uuid
from tipsen.settings import SUPABASE


BUCKET_NAME = "payment"
BUCKET_NAME_2 = "product"
sb = supabase.create_client(supabase_url=SUPABASE["url"], supabase_key=SUPABASE["key"])


def products(request):
    products = Product.objects.all()

    return render(request, "products/index.html", context={"products": products})


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    if not product:
        return redirect("home")

    return render(request, "products/detail.html", context={"product": product})


@login_required
def admin_products(request):
    if not request.user.is_admin:
        return redirect("home")

    products = Product.objects.all()
    return render(request, "products/admin-index.html", context={"products": products})


@login_required
def admin_product(request, product_id):
    if not request.user.is_admin:
        return redirect("home")

    product = Product.objects.get(id=product_id)
    if not product:
        return redirect("home")

    return render(request, "products/admin-detail.html", context={"product": product})


@login_required
def admin_create(request):
    if not request.user.is_admin:
        return redirect("home")
    
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]

            image_data = BufferedReader(image.file)
            random_filename = str(uuid.uuid4()) + "_" + image.name

            content_type, encoding = mimetypes.guess_type(image.name)
            file_options = {"content-type": content_type} if content_type else {}

            response = sb.storage.from_(BUCKET_NAME_2).upload(
                path=random_filename, file=image_data, file_options=file_options
            )

            if response.status_code == 201 or response.status_code == 200:
                image_link = f"{SUPABASE['url']}/storage/v1/object/public/{BUCKET_NAME_2}/{random_filename}"
            else:
                return "Failed to create payment"
            
            Product.objects.create(
                name=request.POST["name"],
                price=request.POST["price"],
                description=request.POST["description"],
                image_link=image_link,
            ).save()

            return render(request, "products/admin-create.html", context={"success": True})

    return render(request, "products/admin-create.html")

@login_required
def admin_delete(request, product_id):
    if not request.user.is_admin:
        return redirect("home")
    
    product = Product.objects.get(id=product_id)
    if not product:
        return redirect("home")
    
    sb.storage.from_(BUCKET_NAME_2).remove(product.image_link.split("/")[-1])
    product.delete()
    
    return redirect("admin-products")
    



@login_required
def order_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if not product:
        return redirect("home")

    addresses = Address.objects.all()
    banks = ["BCA", "Mandiri", "BNI"]

    if request.method == "POST":
        print(request.POST)
        if request.POST.get("step") == "first":
            first_form = OrderFirstForm(request.POST)
            if first_form.is_valid():
                address_id = first_form.cleaned_data["address_id"]
                address = Address.objects.get(id=address_id)
                if not address or address.user_id != request.user._wrapped.id:
                    return render(
                        request,
                        "products/form-before-payment.html",
                        context={
                            "product": product,
                            "addresses": addresses,
                            "error": True,
                            "message": f"couldn't find address with id {address_id}",
                        },
                    )
                quantity = first_form.cleaned_data["quantity"]
                total_price = product.price * quantity
                print(total_price, quantity)

                # Save order data in session
                request.session["address_id"] = address_id
                request.session["quantity"] = quantity
                request.session["total_price"] = total_price
                return render(
                    request,
                    "products/form-after-payment.html",
                    context={
                        "product": product,
                        "addresses": addresses,
                        "banks": banks,
                    },
                )
            else:
                print(first_form.errors)
                return render(
                    request,
                    "products/form-before-payment.html",
                    context={
                        "product": product,
                        "addresses": addresses,
                        "form": first_form,
                    },
                )
        else:
            second_form = OrderSecondForm(request.POST)
            if second_form.is_valid():
                try:
                    # Retrieve order data from session
                    address_id = request.session.get("address_id")
                    quantity = request.session.get("quantity")
                    total_price = request.session.get("total_price")

                    address = Address.objects.get(id=address_id)
                    if not address or address.user_id != request.user._wrapped.id:
                        return render(
                            request,
                            "products/form-before-payment.html",
                            context={
                                "product": product,
                                "addresses": addresses,
                                "error": True,
                                "message": f"couldn't find address with id {address_id}",
                            },
                        )

                    payment = handle_payment_creation(request)

                    Order.objects.create(
                        product=product,
                        quantity=quantity,
                        status="Menunggu Verifikasi Pembayaran",
                        description="",
                        address=address,
                        subtotal=total_price,
                        user=request.user._wrapped,
                        payment=payment,
                    ).save()

                    del request.session["address_id"]
                    del request.session["quantity"]
                    del request.session["total_price"]

                    # TODO: ganti redirect ke "pesanan saya"
                    return redirect("home")
                except Exception as e:
                    return render(
                        request,
                        "products/form-after-payment.html",
                        context={
                            "product": product,
                            "addresses": addresses,
                            "exception_error": {e},
                            "banks": banks,
                        },
                    )
            else:
                print(second_form.errors)
                return render(
                    request,
                    "products/form-after-payment.html",
                    context={
                        "product": product,
                        "addresses": addresses,
                        "form": OrderSecondForm,
                        "banks": banks,
                    },
                )

    return render(
        request,
        "products/form-before-payment.html",
        context={"product": product, "addresses": addresses},
    )

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

        total_price = request.session.get("total_price")

        payment = Payment.objects.create(
            payment_reference_number=request.POST["payment_reference_number"],
            jumlah=total_price,
            bank=request.POST["bank"],
            image_link=image_link,
        )

        payment.save()
        return payment
