from django.contrib import admin

from .models import FeedbackMessage


class FeedbackMessageAdmin(admin.ModelAdmin):
    ...
    

admin.site.register(FeedbackMessage, FeedbackMessageAdmin)