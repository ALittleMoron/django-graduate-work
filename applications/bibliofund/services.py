import os
from typing import Optional


from django.contrib.auth import get_user_model
from django.db.models import Q
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


# TODO: Вынести все эти функции в одну. Тут много повторяющегося кода.
def get_documents_by_user(username: str) -> QuerySet:
    """ Возвращает QuarySet документов по юзернейму со связыванием категорий. """
    return models.Document.objects.filter(publisher__username=username).select_related('category')


def get_documents_by_category(category_slug: str) -> QuerySet:
    """ Возвращает QuarySet документов по категории. """
    return models.Document.objects.filter(category__slug=category_slug).select_related('category')


def get_all_documents() -> QuerySet:
    """ Возвращает QuarySet всех опубликованных документов. """
    return models.Document.objects.filter(is_published=True).select_related('category', 'publisher')


def get_searched_documents_by_param(param: str) -> QuerySet:
    """ Возвращает QuarySet всех опубликованных документов по названию, имени категории или имени
    пользователя. """
    return models.Document.objects.filter(
        Q(is_published=True),
        Q(title__icontains=param) | Q(category__name__icontains=param) |
        Q(publisher__username=param),
        ).select_related('category', 'publisher')


def get_document(doc_slug: str) -> QuerySet:
    """ Возвращает документ по слагу. """
    return models.Document.objects.filter(
        slug=doc_slug
    ).select_related('category', 'publisher')