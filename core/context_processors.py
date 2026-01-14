from orders.cart import get_cart

def cart_counts(request):
    cart = get_cart(request.session)
    total_qty = sum(cart.values()) if cart else 0
    unique_items = len(cart.keys()) if cart else 0
    return {"cart_total_qty": total_qty, "cart_unique_items": unique_items}
