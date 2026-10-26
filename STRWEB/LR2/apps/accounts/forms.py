from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
from .validators import validate_age_18, validate_phone_by


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date', 'required': True}),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': '+375 (29) 123-45-67',
                'pattern': r'\+375\s\((25|29|33|44)\)\s\d{3}-\d{2}-\d{2}',
                'required': True,
            }
        ),
    )
    timezone = forms.ChoiceField(
        label='Часовой пояс',
        choices=[
            ('Europe/Minsk', 'Europe/Minsk (UTC+3)'),
            ('UTC', 'UTC'),
            ('Europe/Moscow', 'Europe/Moscow (UTC+3)'),
        ],
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'phone', 'timezone')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'На эту почту уже зарегистрирован другой пользователь.'
            )
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_age_18(birth_date)
        return birth_date

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        validate_phone_by(phone)
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                birth_date=self.cleaned_data['birth_date'],
                phone=self.cleaned_data['phone'],
                timezone=self.cleaned_data['timezone'],
            )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'timezone', 'avatar')
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'pattern': r'\+375\s\((25|29|33|44)\)\s\d{3}-\d{2}-\d{2}',
                    'placeholder': '+375 (29) 123-45-67',
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        validate_phone_by(phone)
        return phone


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
