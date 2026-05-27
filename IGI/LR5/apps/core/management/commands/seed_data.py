from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import Profile
from apps.catalog.models import Amenity, Category, Employee, Owner, Property, Sale
from apps.core.models import CompanyInfo, ContactEmployee, FAQ, News, PrivacyPolicy, Vacancy
from apps.promo.models import PromoCode
from apps.reviews.models import Review


class Command(BaseCommand):
    help = 'Заполняет БД данными риэлтерского агентства (10+ записей)'

    def handle(self, *args, **options):
        buyer_group, _ = Group.objects.get_or_create(name='Buyer')
        employee_group, _ = Group.objects.get_or_create(name='Employee')

        users = []
        for i in range(1, 11):
            user, created = User.objects.get_or_create(
                username=f'buyer{i}',
                defaults={'email': f'buyer{i}@rieltpro.by', 'first_name': f'Покупатель{i}'},
            )
            if created:
                user.set_password('password123')
                user.save()
            buyer_group.user_set.add(user)
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'birth_date': f'{1985 + (i % 15)}-0{(i % 9) + 1}-10',
                    'phone': f'+375 (29) 300-00-{i:02d}',
                    'timezone': 'Europe/Minsk',
                },
            )
            users.append(user)

        staff_users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'employee{i}',
                defaults={'email': f'emp{i}@rieltpro.by', 'is_staff': True},
            )
            if created:
                user.set_password('password123')
                user.save()
            else:
                user.is_staff = True
                user.save()
            employee_group.user_set.add(user)
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'birth_date': f'{1980 + i}-03-15',
                    'phone': f'+375 (33) 400-00-{i:02d}',
                    'timezone': 'Europe/Minsk',
                },
            )
            Employee.objects.update_or_create(
                user=user,
                defaults={'position': 'Риэлтор', 'department': 'Коммерческий'},
            )
            staff_users.append(user)

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@rieltpro.by', 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        Profile.objects.update_or_create(
            user=admin,
            defaults={
                'birth_date': '1975-01-20',
                'phone': '+375 (29) 111-11-11',
                'timezone': 'Europe/Minsk',
            },
        )
        Employee.objects.update_or_create(
            user=admin,
            defaults={'position': 'Директор', 'department': 'Коммерческий'},
        )

        CompanyInfo.objects.all().delete()
        CompanyInfo.objects.create(
            title='КрышаРиэлт',
            description='Риэлтерское агентство — продажа недвижимости через Интернет.',
            history='Работаем с 2012 года. Коммерческий отдел отслеживает финансовые показатели.',
            phone='+375 (17) 300-00-00',
            email='info@rieltpro.by',
            address='г. Минск, ул. Недвижимости, 13',
        )
        PrivacyPolicy.objects.all().delete()
        PrivacyPolicy.objects.create(
            title='Политика конфиденциальности',
            content='Обработка персональных данных клиентов и сотрудников в соответствии с законом РБ.',
        )

        ContactEmployee.objects.all().delete()
        for i in range(1, 11):
            ContactEmployee.objects.create(
                name=f'Сотрудник {i}',
                phone=f'+375 (44) 500-00-{i:02d}',
                email=f'contact{i}@rieltpro.by',
                position=['Риэлтор', 'Юрист', 'Менеджер', 'Оценщик'][i % 4],
            )

        FAQ.objects.all().delete()
        terms = ['Договор купли-продажи', 'Ипотека', 'Оценка', 'Риэлторские услуги', 'Комиссия']
        for i in range(1, 11):
            term = terms[i % len(terms)]
            FAQ.objects.create(
                question=f'Что такое {term}?',
                answer=f'Определение термина «{term}» в контексте недвижимости.',
            )

        News.objects.all().delete()
        for i in range(1, 11):
            News.objects.create(
                title=f'Новость рынка недвижимости #{i}',
                short_description=f'Краткая сводка по рынку недвижимости — выпуск {i}.',
                content=f'Полный текст аналитической статьи номер {i}.',
                author=admin,
            )

        Vacancy.objects.all().delete()
        for i in range(1, 8):
            Vacancy.objects.create(
                title=f'Риэлтор {i}',
                description=f'Вакансия в коммерческом отделе #{i}.',
                salary=Decimal('1500') + i * 200,
                is_active=True,
            )
        for i in range(8, 11):
            Vacancy.objects.create(
                title=f'Архивная вакансия {i}',
                description='Закрыта.',
                salary=Decimal('1000'),
                is_active=False,
            )

        Category.objects.all().delete()
        cat_names = ['Квартира', 'Дом', 'Коттедж', 'Офис', 'Склад', 'Участок', 'Таунхаус', 'Студия', 'Коммерческая', 'Новостройка']
        categories = [Category.objects.create(name=n, description=f'Категория: {n}') for n in cat_names]

        Amenity.objects.all().delete()
        amenity_names = ['Парковка', 'Лифт', 'Балкон', 'Ремонт', 'Мебель', 'Охрана', 'Интернет', 'Кондиционер', 'Кладовая', 'Терраса']
        amenities = [Amenity.objects.create(name=n) for n in amenity_names]

        Owner.objects.all().delete()
        owners = []
        for i in range(1, 11):
            owners.append(Owner.objects.create(
                full_name=f'Владелец {i}',
                phone=f'+375 (25) 600-00-{i:02d}',
                email=f'owner{i}@mail.by',
                birth_date=f'{1970 + i}-06-15',
                address=f'г. Минск, ул. Владельская, {i}',
            ))

        Property.objects.all().delete()
        properties = []
        for i in range(1, 13):
            prop = Property.objects.create(
                title=f'Объект недвижимости {i}',
                price=Decimal('50000') + i * 15000,
                description=f'Продаётся объект #{i} в отличном состоянии.',
                characteristics=f'Площадь: {40 + i * 5} м², комнат: {i % 4 + 1}, этаж: {i % 10 + 1}',
                category=categories[(i - 1) % len(categories)],
                owner=owners[(i - 1) % len(owners)],
                employee=staff_users[i % len(staff_users)],
                is_sold=i > 2,
            )
            prop.amenities.set(amenities[max(0, (i - 1) % len(amenities) - 1):(i - 1) % len(amenities) + 2])
            properties.append(prop)

        PromoCode.objects.all().delete()
        now = timezone.now()
        for i in range(1, 11):
            PromoCode.objects.create(
                code=f'REALTY{i:02d}',
                discount_percent=3 + i,
                description=f'Скидка на услуги агентства — {i}%',
                is_active=i <= 7,
                valid_until=now + timedelta(days=20 * i),
            )

        Review.objects.all().delete()
        for i in range(1, 11):
            Review.objects.create(
                user=users[i - 1],
                property_obj=properties[i + 1],
                rating=(i % 5) + 1,
                text=f'Отличный объект недвижимости номер {i}, рекомендую!',
            )

        Sale.objects.all().delete()
        for i in range(1, 11):
            prop = properties[i + 1]
            Sale.objects.create(
                property_obj=prop,
                buyer=users[i - 1],
                employee=prop.employee,
                sale_date=(now - timedelta(days=10 * i)).date(),
                contract_date=(now - timedelta(days=(10 * i + 5))).date(),
                amount=prop.price - Decimal(i * 100),
            )

        self.stdout.write(self.style.SUCCESS('Готово! admin/admin123, buyer1/password123, employee1/password123'))
