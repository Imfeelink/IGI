import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.decorators import staff_required

from .forms import BuyerPurchaseForm, OwnerForm, PropertyForm, SaleForm
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
