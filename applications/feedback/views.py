from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import FeedbackForm


class MessageCreateView(CreateView):
    template_name = 'feedback/feedback_form.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('graduateWork/homePage')