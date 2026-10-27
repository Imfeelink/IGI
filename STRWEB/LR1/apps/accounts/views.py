from datetime import date

import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from zoneinfo import ZoneInfo

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import Profile

logger = logging.getLogger('apps.accounts')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info('Registered user %s', user.username)
            messages.success(request, 'Регистрация успешна!')
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info('User %s logged in', user.username)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        logger.info('User %s logged out', username)
        messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('core:home')


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'birth_date': date(1990, 1, 1),
            'phone': '+375 (29) 000-00-00',
            'timezone': 'Europe/Minsk',
        },
    )
    utc_now = timezone.now()
    user_tz = ZoneInfo(profile.timezone)
    local_now = utc_now.astimezone(user_tz)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'accounts/profile.html',
        {
            'form': form,
            'profile': profile,
            'utc_now': utc_now,
            'local_now': local_now,
            'user_timezone': profile.timezone,
        },
    )
