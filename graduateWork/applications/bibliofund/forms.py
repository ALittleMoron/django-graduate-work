from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField

from .models import Document, Category


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'abstract_ru', 'abstract_en', 'document_type', 'category', 'file',)
        widgets = {
            'title': forms.TextInput(attrs={"class": 'form-control'}),
            'abstract_ru': forms.Textarea(attrs={"class": 'form-control'}),
            'abstract_en': forms.Textarea(attrs={"class": 'form-control'}),
        }


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'abstract_ru', 'abstract_en', 'document_type', 'category')
        widgets = {
            'title': forms.TextInput(attrs={"class": 'form-control'}),
            'abstract_ru': forms.Textarea(attrs={"class": 'form-control'}),
            'abstract_en': forms.Textarea(attrs={"class": 'form-control'}),
        }