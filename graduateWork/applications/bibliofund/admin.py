from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static

from .models import Document, Category


class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "document_type",
        "category"
    )
    # list_display_links = ()
    # search_fields = ()
    # list_filter = ()
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'name',
        'category_type'
    )
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(Category, CategoryAdmin)