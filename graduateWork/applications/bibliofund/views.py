from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import View


class HomePage(View):
    """ Класс вывода домашней страницы.
    
    Особо ничего не делает. Только выводит приветственную страницу с навигацией по сайту.
    """
    http_method_names = ['get']
    template_name = 'bibliofund/homePage.html'
    
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)