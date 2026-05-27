from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['property_obj', 'rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
            'text': forms.Textarea(attrs={'required': True, 'minlength': 10, 'rows': 4}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Оценка от 1 до 5.')
        return rating
