import io
import os
import statistics
from datetime import date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from apps.accounts.models import Profile
from apps.catalog.models import Category, Property, Sale


def staff_check(user):
    return user.is_staff or user.is_superuser


def calc_client_ages():
    ages = []
    today = date.today()
    for profile in Profile.objects.select_related('user'):
        bd = profile.birth_date
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        ages.append(age)
    return ages


@login_required
@user_passes_test(staff_check)
def dashboard_view(request):
    amounts = list(Sale.objects.values_list('amount', flat=True))
    total_sales = sum(amounts) if amounts else 0
    mean_amount = statistics.mean(amounts) if amounts else 0
    median_amount = statistics.median(amounts) if amounts else 0
    try:
        mode_amount = statistics.mode(amounts) if amounts else 0
    except statistics.StatisticsError:
        mode_amount = amounts[0] if amounts else 0

    ages = calc_client_ages()
    mean_age = statistics.mean(ages) if ages else 0
    median_age = statistics.median(ages) if ages else 0

    properties_alpha = Property.objects.order_by('title')
    clients_alpha = User.objects.filter(purchases__isnull=False).distinct().order_by('username')

    popular_category = (
        Category.objects.annotate(sales_count=Count('properties__sales'))
        .order_by('-sales_count')
        .first()
    )
    profitable_category = (
        Category.objects.annotate(revenue=Sum('properties__sales__amount'))
        .order_by('-revenue')
        .first()
    )

    sales_by_month = (
        Sale.objects.annotate(month=TruncMonth('sale_date'))
        .values('month')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('month')
    )
    sales_by_category = (
        Category.objects.annotate(revenue=Sum('properties__sales__amount'))
        .values('name', 'revenue')
        .order_by('-revenue')
    )

    chart_sales = generate_sales_chart(sales_by_month)
    chart_categories = generate_revenue_chart(sales_by_category)

    return render(request, 'analytics/dashboard.html', {
        'total_sales': total_sales,
        'mean_amount': mean_amount,
        'median_amount': median_amount,
        'mode_amount': mode_amount,
        'mean_age': mean_age,
        'median_age': median_age,
        'properties_alpha': properties_alpha,
        'clients_alpha': clients_alpha,
        'popular_category': popular_category,
        'profitable_category': profitable_category,
        'chart_sales': chart_sales,
        'chart_categories': chart_categories,
        'total_properties': Property.objects.count(),
        'total_sales_count': Sale.objects.count(),
    })


def generate_sales_chart(data):
    labels, values = [], []
    for row in data:
        if row['month']:
            labels.append(row['month'].strftime('%m/%Y'))
            values.append(float(row['total'] or 0))
    if not labels:
        labels, values = ['Нет данных'], [0]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(labels, values, marker='o', color='#198754')
    ax.set_title('Сумма сделок по месяцам')
    ax.set_ylabel('BYN')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return _save_chart(fig, 'sales.png')


def generate_revenue_chart(data):
    labels = [row['name'] for row in data if row['revenue']] or ['Нет данных']
    values = [float(row['revenue'] or 0) for row in data if row['revenue']] or [0]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color='#0d6efd')
    ax.set_title('Выручка по категориям недвижимости')
    ax.set_ylabel('BYN')
    plt.xticks(rotation=30)
    plt.tight_layout()
    return _save_chart(fig, 'categories.png')


def _save_chart(fig, filename):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    os.makedirs('static/images/charts', exist_ok=True)
    path = f'static/images/charts/{filename}'
    with open(path, 'wb') as f:
        f.write(buf.getvalue())
    return f'/static/images/charts/{filename}'
