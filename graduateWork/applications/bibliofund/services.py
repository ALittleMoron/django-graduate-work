import os

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

from .models import Document

User = get_user_model()


def custom_upload_to(instance, filename: str) -> str:
    """ Кастомная функция для создания пути к загруженному файлу.
    
    Формат для Document: 'documents/user_{username}/filename'
    """
    folder = f'{instance.__class__.__name__.lower()}s'
    user_folder = f'user_{instance.publisher.get_username()}'
    return os.path.join(folder, user_folder, filename)


def get_documents_list_by_user(username: str) -> QuerySet:
    """ Возвращает QuarySet документов по юзернейму со связыванием категорий. """

    return Document.objects.filter(publisher__username=username).prefetch_related('category')
