"""Session-based shopping cart helpers."""

from decimal import Decimal

from .models import Property

CART_SESSION_KEY = 'cart'


def get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def cart_add(session, property_id, quantity=1):
    cart = get_cart(session)
    key = str(property_id)
    cart[key] = cart.get(key, 0) + quantity
    if cart[key] < 1:
        cart.pop(key, None)
    save_cart(session, cart)
    return cart


def cart_set_quantity(session, property_id, quantity):
    cart = get_cart(session)
    key = str(property_id)
    if quantity < 1:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    save_cart(session, cart)
    return cart


def cart_remove(session, property_id):
    cart = get_cart(session)
    cart.pop(str(property_id), None)
    save_cart(session, cart)
    return cart


def cart_clear(session):
    session.pop(CART_SESSION_KEY, None)
    session.modified = True


def cart_items(session):
    """Return list of dicts: property, quantity, line_total; and grand total."""
    cart = get_cart(session)
    items = []
    total = Decimal('0')
    ids = [int(pk) for pk in cart.keys() if str(pk).isdigit()]
    props = {p.pk: p for p in Property.objects.filter(pk__in=ids, is_sold=False)}
    for pk_str, qty in cart.items():
        try:
            pk = int(pk_str)
        except (TypeError, ValueError):
            continue
        prop = props.get(pk)
        if not prop:
            continue
        line = prop.price * qty
        total += line
        items.append({'property': prop, 'quantity': qty, 'line_total': line})
    return items, total


def cart_count(session):
    return sum(get_cart(session).values())
