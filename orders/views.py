from django.conf import settings
from django.shortcuts import redirect, render
from urllib.parse import quote

from .cart import add_to_cart, set_qty, clear_cart, cart_items
from .forms import CheckoutForm
from .models import Order, OrderItem

def cart_view(request):
    items, total, savings_total = cart_items(request.session)
    return render(request, "orders/cart.html", {"items": items, "total": total, "savings_total": savings_total})

def cart_add(request, product_id):
    if request.method == "POST":
        qty = int(request.POST.get("qty", 1))
        add_to_cart(request.session, product_id, qty=qty)
    return redirect("cart")

def cart_remove(request, product_id):
    set_qty(request.session, product_id, 0)
    return redirect("cart")

def cart_update(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("qty_"):
                pid = int(key.replace("qty_", ""))
                try:
                    qty = int(value)
                except ValueError:
                    qty = 1
                set_qty(request.session, pid, qty)
    return redirect("cart")

def checkout_view(request):
    items, total, savings_total = cart_items(request.session)
    if not items:
        return redirect("home")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                notes=form.cleaned_data["notes"],
                total=total,
            )

            for it in items:
                OrderItem.objects.create(
                    order=order,
                    product_name=it["name"],
                    unit_price=it["unit_price"],
                    qty=it["qty"],
                    line_total=it["line_total"],
                )

            store = getattr(settings, "STORE_NAME", "Store")
            currency = getattr(settings, "CURRENCY", "EGP")

            lines = []
            lines.append(f"طلب جديد - {store}")
            lines.append(f"رقم الطلب: #{order.id}")
            lines.append("---- بيانات العميل ----")
            lines.append(f"الاسم: {order.full_name}")
            lines.append(f"الهاتف: {order.phone}")
            lines.append(f"العنوان: {order.address}")
            if order.notes:
                lines.append(f"ملاحظات: {order.notes}")

            if savings_total and savings_total > 0:
                lines.append(f"خصم: {savings_total} {currency}")

            lines.append("---- الطلبات ----")
            for it in order.items.all():
                lines.append(f"- {it.product_name} × {it.qty} = {it.line_total} {currency}")

            lines.append("---- الإجمالي ----")
            lines.append(f"{order.total} {currency}")
            lines.append("الدفع: كاش عند الاستلام")

            msg = "\n".join(lines)

            clear_cart(request.session)

            wa_number = settings.WHATSAPP_NUMBER
            wa_url = f"https://wa.me/{wa_number}?text={quote(msg)}"
            return redirect(wa_url)
    else:
        form = CheckoutForm()

    return render(request, "orders/checkout.html", {"items": items, "total": total, "savings_total": savings_total, "form": form})
