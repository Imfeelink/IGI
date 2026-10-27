from apps.catalog.cart import cart_count


def site_context(request):
    return {
        'site_name': 'РиэлтПрайм',
        'cart_count': cart_count(request.session) if hasattr(request, 'session') else 0,
    }
