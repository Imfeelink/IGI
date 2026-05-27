from django import forms

from .models import News, Vacancy


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'short_description', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'required': True, 'minlength': 3}),
            'short_description': forms.Textarea(attrs={'required': True, 'rows': 3}),
            'content': forms.Textarea(attrs={'required': True, 'rows': 6}),
        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'salary', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'description': forms.Textarea(attrs={'required': True, 'rows': 5}),
        }
