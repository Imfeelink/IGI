from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CompanyInfo(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    history = models.TextField('История')
    logo = models.ImageField('Логотип', upload_to='company/', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=300)
    video_url = models.URLField(
        'Видео (URL iframe/YouTube)',
        blank=True,
        help_text='Ссылка для iframe, например https://www.youtube.com/embed/...',
    )
    video_file = models.FileField('Видеофайл', upload_to='company/video/', blank=True, null=True)
    audio_file = models.FileField('Аудио', upload_to='company/audio/', blank=True, null=True)
    requisites = models.TextField(
        'Реквизиты',
        blank=True,
        help_text='УНП, р/с, банк и т.д.',
    )
    certificate_text = models.TextField(
        'Текст сертификата',
        blank=True,
    )

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

    def __str__(self):
        return self.title


class CompanyHistoryYear(models.Model):
    """История компании по годам"""

    company = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        related_name='history_years',
        verbose_name='Компания',
    )
    year = models.PositiveIntegerField('Год')
    event = models.TextField('Событие')

    class Meta:
        verbose_name = 'История по году'
        verbose_name_plural = 'История по годам'
        ordering = ['year']

    def __str__(self):
        return f'{self.year}: {self.event[:40]}'


class Banner(models.Model):
    """Рекламные баннеры главной страницы"""

    title = models.CharField('Заголовок', max_length=200)
    image = models.ImageField('Изображение', upload_to='banners/')
    link = models.URLField('Ссылка', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    short_description = models.CharField('Краткое описание', max_length=500)
    content = models.TextField('Полный текст')
    image = models.ImageField('Изображение', upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=300)
    answer = models.TextField('Ответ')
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Термин / FAQ'
        verbose_name_plural = 'Словарь терминов'
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]


class ContactEmployee(models.Model):
    name = models.CharField('ФИО', max_length=150)
    photo = models.ImageField('Фото', upload_to='contacts/', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    position = models.CharField('Должность', max_length=150)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name


class PrivacyPolicy(models.Model):
    title = models.CharField('Заголовок', max_length=200, default='Политика конфиденциальности')
    content = models.TextField('Текст')
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField('Должность', max_length=200)
    description = models.TextField('Описание')
    salary = models.DecimalField('Зарплата', max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Partner(models.Model):
    """Партнеры компании для главной страницы"""

    name = models.CharField("Название компании", max_length=150)
    logo = models.ImageField("Логотип", upload_to="partners/", blank=True, null=True)
    website_url = models.URLField("Ссылка на сайт компании")
    description = models.CharField(
        "Краткое описание", max_length=255, blank=True
    )
    is_active = models.BooleanField("Отображать на сайте", default=True)

    class Meta:
        verbose_name = "Компания-партнер"
        verbose_name_plural = "Партнеры"
        ordering = ["name"]

    def __str__(self):
        return self.name
