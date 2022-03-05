from django.urls import path

from .views import MessageCreateView

urlpatterns = [
    path('', MessageCreateView.as_view(), name='feedbackMSG'),
]
