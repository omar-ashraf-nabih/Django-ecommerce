from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True)[:20]
    return render(request, "catalog/product_list.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})
