import os

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from slugify import slugify


def custom_upload_to(instance, filename):
    """ Кастомная функция для создания пути к загруженному файлу.
    
    Формат для Document: 'documents/user_{username}/filename'
    """
    folder = f'{instance.__class__.__name__.lower()}s'
    user_folder = f'user_{instance.publisher.get_username()}'
    return os.path.join(folder, user_folder, filename)


class Document(models.Model):
    """ Класс модели документа.
    
    Документ - любой текстовый файл. В основном, под ними подразумеваются научные работы,
    контрольные, лабораторные, курсовые и дипломные работы, эссе, лекции, методички, сочинения
    и так далее.
    """
    DOCUMENT_TYPE = [
        (0, 'Не выбран'),
        (1, 'Реферат'),
        (2, 'Дипломная работа'),
        (3, 'Магистерская диссертация'),
        (4, 'Отчет по практике'),
        (5, 'Курсовая работа'),
        (6, 'Курсовая практика'),
        (7, 'Практическая работа'),
        (8, 'Эссе'),
        (9, 'Доклад'),
        (10, 'Лекция'),
        (11, 'Методичка'),
        (12, 'Сочинение'),
        (13, 'Контрольная работа'),
    ]
    
    title = models.CharField(max_length=255, unique=True, verbose_name="Заголовок")
    abstract_ru = models.TextField(verbose_name="Аннотация на русском")
    abstract_en = models.TextField(null=True, blank=True, verbose_name="Аннотация на английском")
    slug = models.SlugField(null=True, max_length=300)
    document_type = models.IntegerField(default=0, choices=DOCUMENT_TYPE, verbose_name='Тип')
    category = models.ForeignKey("Category", verbose_name="Категория", on_delete=models.PROTECT)
    file = models.FileField(upload_to=custom_upload_to, verbose_name="Файл")
    file_format = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        verbose_name="Формат файла"
    )
    publisher = models.ForeignKey(
        get_user_model(),
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано?")

    def get_absolute_url(self):
        return reverse("bibliofund/document-detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return f'{self.title} - {self.document_type}'
    
    def __repr__(self) -> str:
        template = '<Document title="{0}" publisher="{1}" type="{2}">'
        return template.format(
            self.title[:20],
            self.publisher.username or "anon",
            Document.DOCUMENT_TYPE[self.document_type][1]
        )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['updated_at']


class Category(models.Model):
    """ Класс модели категории документа c типом категории.
    
    Реализовано так по причине, что от модели не требуется множественная вложенность 
    (многоуровневое наследование Категории на инстансы своего же класса).
    """
    CATEGORY_TYPE = [
        (0, 'Не выбран'),
        (1, 'Экономические'),
        (2, 'Гуманитарные'),
        (3, 'Юридические'),
        (4, 'Естественно-научные'),
        (5, 'Технические'),
    ]
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    category_type = models.IntegerField(
        default=0,
        choices=CATEGORY_TYPE,
        verbose_name='Тип категории'
    )
    slug = models.SlugField(null=True)

    def get_absolute_url(self):
        return reverse("bibliofund/documents-by-category", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return f'{self.name} - {self.category_type}'
    
    def __repr__(self) -> str:
        template = '<Category name="{0}" category_type="{1}">'
        return template.format(
            self.name[:20],
            Category.CATEGORY_TYPE[self.category_type][1]
        )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"


@receiver(pre_save, sender=Document)
def presave_fields(sender, instance, *args, **kwargs):
    """ Обычный сигнал для изменения времени публикации и добавление формата документа. """
    if instance.is_published and instance.published_at is None:
        instance.published_at = timezone.now()
    elif not instance.is_published and instance.published_at is not None:
        instance.published_at = None
    
    if not instance.file_format and instance.file:
        instance.file_format = instance.file.name.split('.')[-1]
        instance.old_format = instance.file_format
    if instance.file_format != instance.old_format:
        instance.file_format = instance.file.name.split('.')[-1]
    
    instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Document)
def presave_slug(sender, instance, *args, **kwargs):
    """ Обычный сигнал для добавления слага перед сохранением.

    Не использую стандартный встроенный в django slugify, потому что он не работает с кириллицей.
    """
    instance.slug = slugify(instance.name)