from django import template

from bibliofund.models import Document


register = template.Library()


@register.filter
def document_type_verbose(boundField):
    return list(filter(lambda x: x[0] == boundField, Document.DOCUMENT_TYPE))[0][1]