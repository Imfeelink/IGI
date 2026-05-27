from django.db import models


class CompanyInfo(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    history = models.TextField('История')
    logo = models.ImageField('Логотип', upload_to='company/', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=300)

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

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
