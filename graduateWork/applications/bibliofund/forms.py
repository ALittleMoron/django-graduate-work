from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Document


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.",
        widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(
        label='Пароль',
        help_text="Пароль должен быть нераспространенным, не состоять только из цифр, состоять более чем из 8 символов.",
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text="Пароли должны совпадать.",
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'abstract_ru', 'abstract_en', 'document_type', 'category', 'file',)
        widgets = {
            # TODO: виджеты для полей.
        }