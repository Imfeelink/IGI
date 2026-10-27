from django import forms

from .models import Owner, Property, Sale


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'price', 'description', 'characteristics',
            'category', 'owner', 'employee', 'amenities', 'image', 'is_sold',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'required': True, 'minlength': 2}),
            'price': forms.NumberInput(attrs={'required': True, 'min': '0.01', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'required': True, 'rows': 3}),
            'characteristics': forms.Textarea(attrs={'required': True, 'rows': 3}),
            'amenities': forms.CheckboxSelectMultiple,
        }


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['full_name', 'phone', 'email', 'birth_date', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={
                'pattern': r'\+375\s\((25|29|33|44)\)\s\d{3}-\d{2}-\d{2}',
                'placeholder': '+375 (29) 123-45-67',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={'required': True, 'type': 'email'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['property_obj', 'buyer', 'employee', 'sale_date', 'contract_date', 'amount']
        labels = {'property_obj': 'Объект недвижимости'}
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'contract_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'amount': forms.NumberInput(attrs={'required': True, 'min': '0.01', 'step': '0.01'}),
        }


class BuyerPurchaseForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['property_obj', 'sale_date', 'contract_date']
        labels = {'property_obj': 'Объект недвижимости'}
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'contract_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property_obj'].queryset = Property.objects.filter(is_sold=False)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=150)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        help_text='Формат: +375 (29) XXX-XX-XX',
    )
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=[
            ('card', 'Банковская карта'),
            ('erip', 'ЕРИП'),
            ('cash', 'Наличные при сделке'),
        ],
    )
    promo_code = forms.CharField(label='Промокод', max_length=50, required=False)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)
    agree = forms.BooleanField(label='Согласен с условиями оплаты')
