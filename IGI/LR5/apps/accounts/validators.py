import re
from datetime import date

from django.core.exceptions import ValidationError


PHONE_REGEX = re.compile(r'^\+375\s\((25|29|33|44)\)\s\d{3}-\d{2}-\d{2}$')


def validate_age_18(value):
    if value is None:
        raise ValidationError('Укажите дату рождения.')
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Регистрация доступна только пользователям 18+.')


def validate_phone_by(value):
    if value and not PHONE_REGEX.match(value):
        raise ValidationError('Телефон: +375 (29) XXX-XX-XX')
