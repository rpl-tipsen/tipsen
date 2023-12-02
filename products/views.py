from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product
from .forms import *
from userprofile.models import Address


def products(request):
    products = Product.objects.all()
    print(products)

    return render(
        request, "products/index.html", context={"products": products}
    )


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    # if not product:
    #     return render(request, "not_found.html")

    return render(
        request, "products/detail.html", context={"product": product}
    )


def order_before_payment(request, product_id):
    product = Product.objects.get(id=product_id)
    addresses = Address.objects.all()
    # if not product:
    #     return render(request, "not_found.html")
    if request.method == 'POST':
        if 'next' in request.POST:
            first_form = OrderFirstForm(request.POST)
            if first_form.is_valid():
                address = first_form.cleaned_data['address']
                quantity = first_form.cleaned_data['quantity']
                # Calculate total price
                total_price = product.price * quantity
                # Save order data in session
                request.session['address'] = address
                request.session['quantity'] = quantity
                request.session['total_price'] = total_price
                return render(
                    request, "products/form-after-payment.html", context={"product": product, "addresses": addresses, "second_form": OrderSecondForm}
                )
        elif 'submit' in request.POST:
            second_form = OrderSecondForm(request.POST)
            if second_form.is_valid():
                payment_method = second_form.cleaned_data['payment_method']
                payment_reference = second_form.cleaned_data['payment_reference']
                # Retrieve order data from session
                address = request.session.get('address')
                quantity = request.session.get('quantity')
                total_price = request.session.get('total_price')
                # Save order in database
                # order = Order.objects.create(
                #     product=product,
                #     quantity=quantity,
                #     address=address,
                #     total_price=total_price,
                #     # Assign payment details
                #     payment_method=payment_method,
                #     payment_reference=payment_reference
                # )
                del request.session['address']
                del request.session['quantity']
                del request.session['total_price']
                # return redirect('order_confirmation')
    else:
        first_form = OrderFirstForm()
        second_form = OrderSecondForm()
    return render(
        request, "products/form-before-payment.html", context={"product": product, "addresses": addresses, "first_form": first_form}
    )


def order_after_payment(request, product_id, address_id):
    product = Product.objects.get(id=product_id)
    address = Address.objects.get(id=address_id)
    # if not product or not address:
    #     return render(request, "not_found.html")
    return render(
        request, "products/form-after-payment.html", context={"product": product, "address": address}
    )


@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user._wrapped)
    addresses = Address.objects.filter(user=request.user._wrapped)

    # print(addresses[0].__dict__)

    return render(
        request=request,
        template_name="userprofile/profile.html",
        context={"user": {"auth": request.user._wrapped,
                          "profile": user_profile}, "addresses": addresses},
    )


@login_required
def create_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)

            addresses = Address.objects.filter(user=request.user._wrapped)

            if len(addresses) >= 3:
                return render(
                    request=request,
                    template_name="userprofile/address.html",
                    context={
                        "error": True, "message": "Jumlah alamat sudah maksimum (3 alamat)"},
                )

            address.user = request.user._wrapped
            address.save()
            return render(
                request=request,
                template_name="userprofile/address.html",
                context={"success": True,
                         "message": "Berhasil menyimpan alamat"},
            )

    form = AddressForm()
    return render(
        request=request,
        template_name="userprofile/address.html",
        context={"form": form, "url": reverse("create_address")},
    )


@login_required
def update_address(request, address_id: int):
    address = Address.objects.get(id=address_id)

    if not address and address.user_id != request.user._wrapped.id:
        return render(
            request=request,
            template_name="userprofile/address.html",
            context={
                "url": reverse("update_address", kwargs={"address_id": address_id}),
                "address": address,
                "error": True,
                "message": f"couldn't find address with id {address_id}",
            },
        )

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address: Address = form.save(commit=False)
            address.receiver_name = new_address.receiver_name
            address.phone_number = new_address.phone_number
            address.address = new_address.address
            address.city = new_address.city
            address.postal_code = new_address.postal_code
            address.save()

            return render(
                request=request,
                template_name="userprofile/address.html",
                context={"success": True,
                         "message": "Berhasil menyimpan alamat"},
            )

    form = AddressForm()
    return render(
        request=request,
        template_name="userprofile/address.html",
        context={"form": form, "url": reverse(
            "update_address", kwargs={"address_id": address_id}), "address": address},
    )


@login_required
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)

    if not address and address.user_id != request.user._wrapped.id:
        return render(
            request=request,
            template_name="userprofile/address.html",
            context={
                "url": reverse("update_address", kwargs={"address_id": address_id}),
                "address": address,
                "error": True,
                "message": f"couldn't find address with id {address_id}",
            },
        )

    address.delete()
    return render(
        request=request,
        template_name="userprofile/profile.html",
        context={"success": True, "message": "Berhasil menghapus alamat"},
    )
