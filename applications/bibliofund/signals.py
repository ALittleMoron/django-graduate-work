from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from slugify import slugify

from .models import Category, Document, FileStatistic


@receiver(pre_save, sender=Document)
def presave_fields(sender, instance, *args, **kwargs):
    """ Обычный сигнал для изменения времени публикации и добавление формата документа. """
    if instance.is_published and instance.published_at is None:
        instance.published_at = timezone.now()
    elif not instance.is_published and instance.published_at is not None:
        instance.published_at = None
    
    instance.file_format = instance.file.name.split('.')[-1]



@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Document)
def presave_slug(sender, instance, *args, **kwargs):
    """ Обычный сигнал для добавления слага перед сохранением.

    Не использую стандартный встроенный в django slugify, потому что он не работает с кириллицей.
    """
    if instance.__class__.__name__ == "Document":
        instance.slug = slugify(instance.title)
    elif instance.__class__.__name__ == "Category":
        instance.slug = slugify(instance.name)


@receiver(post_save, sender=Document)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        statistic = FileStatistic()
        statistic.save()
        instance.statistic = statistic
        instance.save()