import logging
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.core.decorators import staff_required

from . import cart as cart_helpers
from .forms import BuyerPurchaseForm, CheckoutForm, OwnerForm, PropertyForm, SaleForm
from .models import Owner, Property, Sale

logger = logging.getLogger('apps.catalog')


def property_list_view(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', 'title')
    allowed = {'title', '-title', 'price', '-price', 'created_at', '-created_at'}
    if sort not in allowed:
        sort = 'title'
    properties = Property.objects.select_related('category', 'owner', 'employee').prefetch_related('amenities')
    if q:
        properties = properties.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(characteristics__icontains=q)
        )
    if category_id.isdigit():
        properties = properties.filter(category_id=int(category_id))
    if not request.user.is_staff:
        properties = properties.filter(is_sold=False)
    properties = properties.order_by(sort)
    from .models import Category
    categories = Category.objects.all()
    return render(request, 'catalog/property_list.html', {
        'properties': properties, 'q': q, 'sort': sort,
        'categories': categories, 'category_id': category_id,
    })


def property_detail_view(request, pk):
    prop = get_object_or_404(Property.objects.select_related('category', 'owner', 'employee'), pk=pk)
    return render(request, 'catalog/property_detail.html', {'property': prop})


@staff_required
def property_create_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save()
            logger.info('Property created: %s by %s', prop.title, request.user.username)
            return redirect('catalog:property_list')
    else:
        form = PropertyForm()
    return render(request, 'catalog/property_form.html', {'form': form, 'title': 'Добавить объект'})


@staff_required
def property_update_view(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            return redirect('catalog:property_list')
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'catalog/property_form.html', {'form': form, 'title': 'Редактировать объект'})


@staff_required
def property_delete_view(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        title = prop.title
        prop.delete()
        logger.info('Property deleted: %s', title)
        return redirect('catalog:property_list')
    return render(request, 'catalog/property_confirm_delete.html', {'property': prop})


def owner_list_view(request):
    if not request.user.is_staff:
        return redirect('core:home')
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'full_name')
    owners = Owner.objects.all()
    if q:
        owners = owners.filter(Q(full_name__icontains=q) | Q(email__icontains=q))
    owners = owners.order_by(sort if sort in {'full_name', '-full_name'} else 'full_name')
    return render(request, 'catalog/owner_list.html', {'owners': owners, 'q': q, 'sort': sort})


@staff_required
def owner_create_view(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:owner_list')
    else:
        form = OwnerForm()
    return render(request, 'catalog/owner_form.html', {'form': form, 'title': 'Добавить владельца'})


@staff_required
def owner_update_view(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('catalog:owner_list')
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'catalog/owner_form.html', {'form': form, 'title': 'Редактировать владельца'})


@staff_required
def owner_delete_view(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        owner.delete()
        return redirect('catalog:owner_list')
    return render(request, 'catalog/owner_confirm_delete.html', {'owner': owner})


@login_required
def sale_list_view(request):
    if request.user.is_staff:
        sales = Sale.objects.select_related('property_obj', 'buyer', 'employee')
        if not request.user.is_superuser:
            sales = sales.filter(Q(employee=request.user) | Q(property_obj__employee=request.user))
    else:
        sales = Sale.objects.filter(buyer=request.user).select_related('property_obj', 'employee')
    return render(request, 'catalog/sale_list.html', {'sales': sales})


@staff_required
def sale_create_view(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()
            sale.property_obj.is_sold = True
            sale.property_obj.save(update_fields=['is_sold'])
            logger.info('Sale created: #%s', sale.pk)
            return redirect('catalog:sale_list')
    else:
        form = SaleForm()
    return render(request, 'catalog/sale_form.html', {'form': form, 'title': 'Новая сделка'})


@staff_required
def sale_update_view(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('catalog:sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'catalog/sale_form.html', {'form': form, 'title': 'Редактировать сделку'})


@staff_required
def sale_delete_view(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        prop = sale.property_obj
        sale.delete()
        if not prop.sales.exists():
            prop.is_sold = False
            prop.save(update_fields=['is_sold'])
        return redirect('catalog:sale_list')
    return render(request, 'catalog/sale_confirm_delete.html', {'sale': sale})


@login_required
def purchase_create_view(request):
    if request.user.is_staff:
        return redirect('catalog:sale_create')
    if request.method == 'POST':
        form = BuyerPurchaseForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.buyer = request.user
            sale.amount = sale.property_obj.price
            if sale.property_obj.employee_id:
                sale.employee = sale.property_obj.employee
            sale.save()
            sale.property_obj.is_sold = True
            sale.property_obj.save(update_fields=['is_sold'])
            return redirect('catalog:sale_list')
    else:
        form = BuyerPurchaseForm()
    return render(request, 'catalog/purchase_form.html', {'form': form})


@require_POST
def cart_add_view(request, pk):
    prop = get_object_or_404(Property, pk=pk, is_sold=False)
    cart_helpers.cart_add(request.session, prop.pk, 1)
    messages.success(request, f'«{prop.title}» добавлен в корзину.')
    return redirect('catalog:cart')


def cart_view(request):
    items, total = cart_helpers.cart_items(request.session)
    return render(request, 'catalog/cart.html', {'items': items, 'total': total})


@require_POST
def cart_update_view(request, pk):
    action = request.POST.get('action', '')
    cart = cart_helpers.get_cart(request.session)
    key = str(pk)
    current = cart.get(key, 0)
    if action == 'increase':
        cart_helpers.cart_set_quantity(request.session, pk, current + 1)
    elif action == 'decrease':
        cart_helpers.cart_set_quantity(request.session, pk, current - 1)
    elif action == 'remove':
        cart_helpers.cart_remove(request.session, pk)
        messages.info(request, 'Объект удалён из корзины.')
    return redirect('catalog:cart')


@login_required
def checkout_view(request):
    items, total = cart_helpers.cart_items(request.session)
    if not items:
        messages.warning(request, 'Корзина пуста.')
        return redirect('catalog:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            today = date.today()
            created = 0
            for item in items:
                prop = item['property']
                if prop.is_sold:
                    continue
                amount = prop.price * item['quantity']
                promo = form.cleaned_data.get('promo_code', '').strip()
                if promo:
                    from apps.promo.models import PromoCode
                    try:
                        code = PromoCode.objects.get(code__iexact=promo, is_active=True)
                        discount = Decimal(code.discount_percent) / Decimal('100')
                        amount = (amount * (Decimal('1') - discount)).quantize(Decimal('0.01'))
                    except PromoCode.DoesNotExist:
                        pass
                Sale.objects.create(
                    property_obj=prop,
                    buyer=request.user,
                    employee=prop.employee,
                    sale_date=today,
                    contract_date=today,
                    amount=amount,
                )
                prop.is_sold = True
                prop.save(update_fields=['is_sold'])
                created += 1
            cart_helpers.cart_clear(request.session)
            messages.success(
                request,
                f'Оплата оформлена. Создано сделок: {created}. Способ: {form.cleaned_data["payment_method"]}.',
            )
            logger.info('Checkout by %s: %s sales', request.user.username, created)
            return redirect('catalog:sale_list')
    else:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile') and request.user.profile.phone:
            initial['phone'] = request.user.profile.phone
        form = CheckoutForm(initial=initial)

    return render(request, 'catalog/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
    })
