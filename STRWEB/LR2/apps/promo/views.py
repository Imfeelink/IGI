from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from .models import PromoCode


@login_required
def promo_list_view(request):
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '-valid_until')
    allowed = {'code', '-code', 'discount_percent', '-discount_percent', 'valid_until', '-valid_until'}
    if sort not in allowed:
        sort = '-valid_until'
    promos = PromoCode.objects.all()
    if q:
        promos = promos.filter(Q(code__icontains=q) | Q(description__icontains=q))
    promos = promos.order_by(sort)
    now = timezone.now()
    return render(request, 'promo/promo_list.html', {'promos': promos, 'q': q, 'sort': sort, 'now': now})
