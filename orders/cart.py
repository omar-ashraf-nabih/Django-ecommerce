from decimal import Decimal, ROUND_HALF_UP
from catalog.models import Product

CART_KEY = "cart_v1"

def get_cart(session):
    return session.get(CART_KEY, {})

def save_cart(session, cart):
    session[CART_KEY] = cart
    session.modified = True

def add_to_cart(session, product_id, qty=1):
    cart = get_cart(session)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + int(qty)
    if cart[pid] <= 0:
        cart.pop(pid, None)
    save_cart(session, cart)

def set_qty(session, product_id, qty):
    cart = get_cart(session)
    pid = str(product_id)
    qty = int(qty)
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    save_cart(session, cart)

def clear_cart(session):
    save_cart(session, {})

def _quantize_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def _best_tier(product: Product, qty: int):
    """أفضل خصم: أعلى min_qty بشرط qty >= min_qty."""
    best = None
    for t in product.discount_tiers.all():
        if not t.is_active:
            continue
        if qty >= t.min_qty:
            best = t
    return best

def _effective_unit_price(product: Product, qty: int):
    base_price = _quantize_money(Decimal(product.price))
    tier = _best_tier(product, qty)
    if tier:
        percent = Decimal(tier.percent_off)
        factor = (Decimal("100") - percent) / Decimal("100")
        unit = _quantize_money(base_price * factor)
        return unit, percent, base_price
    return base_price, Decimal("0"), base_price

def cart_items(session):
    cart = get_cart(session)
    ids = [int(k) for k in cart.keys()] if cart else []
    products = Product.objects.filter(id__in=ids, is_active=True).prefetch_related("discount_tiers")
    prod_map = {p.id: p for p in products}

    items = []
    total = Decimal("0.00")
    savings_total = Decimal("0.00")

    for pid_str, qty in cart.items():
        pid = int(pid_str)
        p = prod_map.get(pid)
        if not p:
            continue

        unit_price, percent_off, base_price = _effective_unit_price(p, qty)
        line_total = _quantize_money(unit_price * qty)
        base_line_total = _quantize_money(base_price * qty)
        savings_line = _quantize_money(base_line_total - line_total)

        total += line_total
        savings_total += savings_line

        items.append({
            "id": p.id,
            "name": p.name,
            "base_price": base_price,
            "unit_price": unit_price,
            "percent_off": percent_off,
            "qty": qty,
            "line_total": line_total,
            "savings_line": savings_line,
            "image": p.image.url if p.image else "",
            "slug": p.slug,
        })

    return items, _quantize_money(total), _quantize_money(savings_total)
