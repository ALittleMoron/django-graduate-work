from django.contrib import admin

from .models import Document, Category, FileStatistic


class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "document_type",
        "category",
        "published_at"
    )
    search_fields = ('title', 'abstract_en', 'abstract_ru')
    list_display_links = ('id', 'title',)
    list_filter = ('document_type', 'is_published', 'published_at')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('published_at', 'file_format',)


class FileStatisticAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'name',
        'category_type'
    )
    search_fields = ('name', 'category_type')
    list_display_links = ('id', 'name',)
    list_filter = ('category_type',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(FileStatistic, FileStatisticAdmin)
admin.site.register(Category, CategoryAdmin)