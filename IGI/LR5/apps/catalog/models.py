from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.accounts.validators import validate_age_18, validate_phone_by


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Категория недвижимости'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField('Удобство', max_length=100)

    class Meta:
        verbose_name = 'Удобство'
        verbose_name_plural = 'Удобства'

    def __str__(self):
        return self.name


class Owner(models.Model):
    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=20, validators=[validate_phone_by])
    email = models.EmailField('Email')
    birth_date = models.DateField('Дата рождения', validators=[validate_age_18])
    address = models.CharField('Адрес', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='Пользователь',
    )
    position = models.CharField('Должность', max_length=150)
    department = models.CharField('Отдел', max_length=150, default='Коммерческий')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — {self.position}'


class Property(models.Model):
    title = models.CharField('Название', max_length=200)
    price = models.DecimalField(
        'Цена',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    description = models.TextField('Описание')
    characteristics = models.TextField('Характеристики', help_text='Площадь, этаж, комнаты и т.д.')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name='Категория',
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name='Владелец',
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_properties',
        verbose_name='Ответственный сотрудник',
    )
    amenities = models.ManyToManyField(
        Amenity,
        related_name='properties',
        blank=True,
        verbose_name='Удобства',
    )
    image = models.ImageField('Фото', upload_to='properties/', blank=True, null=True)
    is_sold = models.BooleanField('Продан', default=False)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True)

    class Meta:
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['title']

    def __str__(self):
        return self.title


class Sale(models.Model):
    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Объект',
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупатель',
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sales',
        verbose_name='Сотрудник',
    )
    sale_date = models.DateField('Дата продажи')
    contract_date = models.DateField('Дата договора')
    amount = models.DecimalField('Сумма сделки', max_digits=12, decimal_places=2)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Изменена', auto_now=True)

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        ordering = ['-sale_date']

    def __str__(self):
        return f'Сделка #{self.pk} — {self.property_obj.title}'
