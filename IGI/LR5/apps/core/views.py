import calendar
import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import staff_required
from .forms import NewsForm, VacancyForm
from .models import CompanyInfo, ContactEmployee, FAQ, News, PrivacyPolicy, Vacancy

logger = logging.getLogger('apps.core')


def home_view(request):
    latest_news = News.objects.first()
    return render(request, 'core/home.html', {'latest_news': latest_news})


def about_view(request):
    company = CompanyInfo.objects.first()
    return render(request, 'core/about.html', {'company': company})


def news_list_view(request):
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '-created_at')
    allowed = {'title', '-title', 'created_at', '-created_at'}
    if sort not in allowed:
        sort = '-created_at'
    news = News.objects.all()
    if q:
        news = news.filter(Q(title__icontains=q) | Q(short_description__icontains=q))
    news = news.order_by(sort)
    return render(request, 'core/news_list.html', {'news_list': news, 'q': q, 'sort': sort})


def news_detail_view(request, pk):
    item = get_object_or_404(News, pk=pk)
    return render(request, 'core/news_detail.html', {'news': item})


@staff_required
def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            logger.info('News created: %s by %s', news.title, request.user.username)
            return redirect('core:news_list')
    else:
        form = NewsForm()
    return render(request, 'core/news_form.html', {'form': form, 'title': 'Создать новость'})


@staff_required
def news_update_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            logger.info('News updated: %s', news.title)
            return redirect('core:news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'core/news_form.html', {'form': form, 'title': 'Редактировать новость'})


@staff_required
def news_delete_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        title = news.title
        news.delete()
        logger.info('News deleted: %s', title)
        return redirect('core:news_list')
    return render(request, 'core/news_confirm_delete.html', {'news': news})


def faq_list_view(request):
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '-created_at')
    allowed = {'question', '-question', 'created_at', '-created_at'}
    if sort not in allowed:
        sort = '-created_at'
    faqs = FAQ.objects.all()
    if q:
        faqs = faqs.filter(Q(question__icontains=q) | Q(answer__icontains=q))
    faqs = faqs.order_by(sort)
    return render(request, 'core/faq_list.html', {'faqs': faqs, 'q': q, 'sort': sort})


def contacts_view(request):
    employees = ContactEmployee.objects.all()
    return render(request, 'core/contacts.html', {'employees': employees})


def privacy_view(request):
    policy = PrivacyPolicy.objects.first()
    return render(request, 'core/privacy.html', {'policy': policy})


def vacancy_list_view(request):
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '-created_at')
    allowed = {'title', '-title', 'salary', '-salary', 'created_at', '-created_at'}
    if sort not in allowed:
        sort = '-created_at'
    vacancies = Vacancy.objects.filter(is_active=True)
    if q:
        vacancies = vacancies.filter(Q(title__icontains=q) | Q(description__icontains=q))
    vacancies = vacancies.order_by(sort)
    return render(request, 'core/vacancy_list.html', {'vacancies': vacancies, 'q': q, 'sort': sort})


def vacancy_detail_view(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'core/vacancy_detail.html', {'vacancy': vacancy})


@staff_required
def vacancy_create_view(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:vacancy_list')
    else:
        form = VacancyForm()
    return render(request, 'core/vacancy_form.html', {'form': form, 'title': 'Создать вакансию'})


@staff_required
def vacancy_update_view(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('core:vacancy_list')
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, 'core/vacancy_form.html', {'form': form, 'title': 'Редактировать вакансию'})


@staff_required
def vacancy_delete_view(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    if request.method == 'POST':
        vacancy.delete()
        return redirect('core:vacancy_list')
    return render(request, 'core/vacancy_confirm_delete.html', {'vacancy': vacancy})


def calendar_view(request):
    now = timezone.now()
    cal = calendar.TextCalendar(calendar.MONDAY)
    month_text = cal.formatmonth(now.year, now.month)
    return render(
        request,
        'core/calendar.html',
        {'calendar_text': month_text, 'month_name': now.strftime('%B %Y'), 'now': now},
    )
