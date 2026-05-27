from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Войдите в систему.')
            return redirect('accounts:login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Доступ только для сотрудников.')
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_message(view_func):
    from django.contrib.auth.decorators import login_required
    return login_required(view_func)
