from datetime import date

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.accounts.forms import RegisterForm
from apps.accounts.validators import validate_age_18, validate_phone_by
from apps.catalog.models import Category, Owner, Property, Sale
from apps.core.models import News
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_home_page(client):
    response = client.get(reverse('core:home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_property_list_page(client):
    response = client.get(reverse('catalog:property_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_property_creation():
    category = Category.objects.create(name='Квартира')
    owner = Owner.objects.create(
        full_name='Иванов',
        phone='+375 (29) 123-45-67',
        email='ivan@test.by',
        birth_date=date(1980, 1, 1),
    )
    prop = Property.objects.create(
        title='Квартира 1',
        description='Описание',
        characteristics='50 м²',
        price='100000.00',
        category=category,
        owner=owner,
    )
    assert prop.title == 'Квартира 1'


@pytest.mark.django_db
def test_invalid_birth_date():
    with pytest.raises(ValidationError):
        validate_age_18(date(2015, 1, 1))


def test_valid_phone():
    validate_phone_by('+375 (29) 123-45-67')


def test_invalid_phone():
    with pytest.raises(ValidationError):
        validate_phone_by('80291234567')


@pytest.mark.django_db
def test_register_form_duplicate_email():
    User.objects.create_user(
        username='existing',
        email='same@test.by',
        password='pass12345',
    )
    form = RegisterForm(data={
        'username': 'newuser',
        'email': 'same@test.by',
        'password1': 'ComplexPass123!',
        'password2': 'ComplexPass123!',
        'birth_date': '1990-06-01',
        'phone': '+375 (29) 123-45-67',
        'timezone': 'Europe/Minsk',
    })
    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_register_form_age_validation():
    form = RegisterForm(data={
        'username': 'teen',
        'email': 'teen@test.by',
        'password1': 'ComplexPass123!',
        'password2': 'ComplexPass123!',
        'birth_date': '2015-06-01',
        'phone': '+375 (29) 123-45-67',
        'timezone': 'Europe/Minsk',
    })
    assert not form.is_valid()


@pytest.mark.django_db
def test_login(client):
    User.objects.create_user(username='testuser', password='pass12345')
    response = client.post(reverse('accounts:login'), {
        'username': 'testuser',
        'password': 'pass12345',
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(client):
    User.objects.create_user(username='testuser', password='pass12345')
    client.login(username='testuser', password='pass12345')
    response = client.get(reverse('accounts:logout'))
    assert response.status_code == 302
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_api_requires_auth(client):
    response = client.get(reverse('api:external_data'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_promo_requires_auth(client):
    response = client.get(reverse('promo:promo_list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_privacy_page(client):
    response = client.get(reverse('core:privacy'))
    assert response.status_code == 200
