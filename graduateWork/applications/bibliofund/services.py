import os
from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

import bibliofund.models as models


User = get_user_model()


def custom_upload_to(instance, filename: str) -> str:
    """ Кастомная функция для создания пути к загруженному файлу.
    
    Формат для Document: 'documents/user_{username}/filename'
    """
    folder = f'{instance.__class__.__name__.lower()}s'
    user_folder = f'user_{instance.publisher.get_username()}'
    return os.path.join(folder, user_folder, filename)


def get_documents_by_user(username: str) -> QuerySet:
    """ Возвращает QuarySet документов по юзернейму со связыванием категорий. """
    return models.Document.objects.filter(publisher__username=username).prefetch_related('category')


def get_documents_by_category(category_name: str) -> QuerySet:
    """ Возвращает QuarySet документов по категории. """
    return models.Document.objects.filter(category__name=category_name).prefetch_related('category')


def get_all_documents() -> QuerySet:
    """ Возвращает QuarySet всех опубликованных документов. """
    return models.Document.objects.filter(is_published=True).prefetch_related('category')
