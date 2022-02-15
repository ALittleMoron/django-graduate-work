from django.apps import AppConfig


class BibliofundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bibliofund'
    verbose_name = 'Библиофонд'

    def ready(self):
        import bibliofund.signals