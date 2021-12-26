from django import template
from django.db.models import Count

from bibliofund.models import Document, Category


register = template.Library()


@register.filter
def document_type_verbose(boundField):
    return list(filter(lambda x: x[0] == boundField, Document.DOCUMENT_TYPE))[0][1]


@register.simple_tag
def get_all_categories():
    return Category.objects.annotate(num_docs=Count('document')).all()