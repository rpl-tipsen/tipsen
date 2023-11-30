from .models import UserProfile, Address
from .forms import AddressForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user._wrapped)
    addresses = Address.objects.filter(user=request.user._wrapped)

    print(addresses[0].__dict__)

    return render(
        request=request,
        template_name="userprofile/profile.html",
        context={"user": {"auth": request.user._wrapped, "profile": user_profile}, "addresses": addresses},
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
                    context={"error": True, "message": "Jumlah alamat sudah maksimum (3 alamat)"},
                )

            address.user = request.user._wrapped
            address.save()
            return render(
                request=request,
                template_name="userprofile/address.html",
                context={"success": True, "message": "Berhasil menyimpan alamat"},
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
                context={"success": True, "message": "Berhasil menyimpan alamat"},
            )

    form = AddressForm()
    return render(
        request=request,
        template_name="userprofile/address.html",
        context={"form": form, "url": reverse("update_address", kwargs={"address_id": address_id}), "address": address},
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
