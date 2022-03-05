from django import forms

from .models import FeedbackMessage

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = ('full_name', 'email', 'message')
        widgets = {
            'full_name': forms.TextInput(attrs={"class": 'form-control'}),
            'email': forms.TextInput(attrs={"class": 'form-control'}),
            'message': forms.Textarea(attrs={"class": 'form-control'}),
        }