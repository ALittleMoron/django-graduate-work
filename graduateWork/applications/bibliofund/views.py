from django.db.models import query
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import CreateView, FormView, ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .services import get_documents_list_by_user


class UserAccountView(ListView):
    """  """

    tempate_name = 'bibliofund/auth/account.html'
    paginate_by = 10
    
    def get_queryset(self):
        self.queryset = get_documents_list_by_user(self.kwargs.get('username'))
        return super().get_queryset()
        # TODO : Проверить на работоспособность. Получает ли функция имя пользователя.
    

class UserLoginView(LoginView):
    """ Класс обработки входа пользователя в систему. """
    
    template_name = 'bibliofund/auth/login.html'
    authentication_form = CustomAuthenticationForm


class UserRegisterView(CreateView, FormView):
    """ Класс обработки регистрации пользователя в системе. """
    
    template_name = 'bibliofund/auth/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('graduateWork/login')


class HomePageView(View):
    """ Класс вывода домашней страницы. """
    
    http_method_names = ['get']
    template_name = 'bibliofund/homePage.html'
    
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)


class DocumentByCategoryView(ListView):
    """ Класс вывода документов по выбранной категории. """
    
    pass


class DocumentDetailView(DetailView):
    """ Класс вывода подробной информации одного документа. """
    
    pass
