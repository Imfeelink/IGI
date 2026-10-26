from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    code = models.CharField('Код', max_length=50, unique=True)
    discount_percent = models.PositiveSmallIntegerField('Скидка %')
    description = models.CharField('Описание', max_length=300)
    is_active = models.BooleanField('Активен', default=True)
    valid_until = models.DateTimeField('Действует до')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды и купоны'
        ordering = ['-valid_until']

    def __str__(self):
        status = 'активен' if self.is_active else 'архив'
        return f'{self.code} ({status})'

    @property
    def is_valid_now(self):
        return self.is_active and self.valid_until >= timezone.now()
