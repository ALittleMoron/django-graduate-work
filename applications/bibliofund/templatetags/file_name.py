from django import template
from django.db.models import Count

from bibliofund.models import Document, Category


register = template.Library()


@register.filter
def get_file_name(fl: str):
    return fl.split('/')[-1]