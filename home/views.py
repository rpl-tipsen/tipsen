from django.shortcuts import render
from products.models import Product


def home(request):
    query = request.GET.get("query", "")

    if query == "":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=query)
    return render(request, "home/index.html", {"products": products})

