from django.conf import settings
from django.db import models

from .validators import validate_age_18, validate_phone_by


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    birth_date = models.DateField('Дата рождения', validators=[validate_age_18])
    phone = models.CharField('Телефон', max_length=20, validators=[validate_phone_by])
    timezone = models.CharField('Часовой пояс', max_length=64, default='Europe/Minsk')
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'
