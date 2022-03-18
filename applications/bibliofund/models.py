from tabnanny import verbose
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .services import custom_upload_to


class FileStatistic(models.Model):
    """ Класс модели статистики файла. """
    download_count = models.IntegerField(
        default=0,
        verbose_name='Количество скачиваний'
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )

    def increment_field(self, field_name: str) -> None:
        setattr(self, field_name, models.F(field_name) + 1)
        self.save(update_fields=[field_name])
    
    def __str__(self) -> str:
        return f"Статистика {self.pk}: {self.download_count} скачивание, {self.view_count} просмотр"

    class Meta:
        verbose_name = "Стасистика"
        verbose_name_plural = "Статистики"
        ordering = ["-view_count"]


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
        (11, 'Методические пособия'),
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
    statistic = models.OneToOneField(
        FileStatistic,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        return reverse("graduateWork/documentDetail", kwargs={"slug": self.slug})

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
        return reverse("graduateWork/documentsByCategory", kwargs={"slug": self.slug})

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

