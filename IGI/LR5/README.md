# ЛР5 — Вариант 13: Риэлтерское агентство (КрышаРиэлт)

Django-приложение для продажи недвижимости через Интернет с отслеживанием финансовых показателей коммерческого отдела.

## Предметная область

- **Объекты недвижимости** — название, цена, характеристики, категория, владелец
- **Категории** — квартира, дом, офис и т.д.
- **Владельцы** — анкетные данные, телефон, email (18+)
- **Покупатели** — зарегистрированные пользователи (группа Buyer)
- **Сотрудники** — staff + модель Employee (группа Employee)
- **Продажи** — клиент, дата продажи, дата договора, сумма

## Связи моделей

- `OneToOne`: User ↔ Profile, User ↔ Employee
- `ForeignKey`: Property → Category, Owner, Employee; Sale → Property, Buyer, Employee
- `ManyToMany`: Property ↔ Amenity

## Роли

| Роль | Доступ |
|------|--------|
| Гость | Главная, новости, каталог (доступные объекты), FAQ, контакты, политика, вакансии |
| Покупатель (User) | + промокоды, отзывы, покупки, API, личный кабинет |
| Сотрудник (staff) | + CRUD объектов/владельцев/сделок, аналитика |
| Superuser | Полный доступ + админка |

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Учётные записи (после seed_data)

| Логин | Пароль | Роль |
|-------|--------|------|
| admin | admin123 | superuser |
| employee1 | password123 | сотрудник |
| buyer1 | password123 | покупатель |

## Docker

```bash
docker-compose up --build
```

PostgreSQL в Docker, SQLite локально без `DATABASE_URL`.

## Тесты

```bash
pytest
```

## GitHub

Репозиторий для проверки: добавить доступ `@AnnBsuir` (anzh52889@gmail.com).

## Деплой

Render / Railway с переменными: `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`.
