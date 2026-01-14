from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout_view, name="checkout"),
]
