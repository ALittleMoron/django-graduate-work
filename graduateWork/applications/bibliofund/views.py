from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import CreateView, FormView, ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Document
from .services import get_all_documents, get_documents_by_category, get_documents_by_user


class UserAccountView(ListView):
    """ Класс обработки работы с аккаунтом пользователя. 
    
    Унаследован от ListView для того, чтобы было удобно выводить все документы пользователя.
    """

    template_name = 'bibliofund/account.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        self.queryset = get_documents_by_user(self.kwargs.get('username'))
        return super().get_queryset()


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


class AllDocumentsView(ListView):
    """ Класс вывода всех опубликованных документов. """
    
    template_name = 'bibliofund/allDocuments.html'
    context_object_name = 'documents'
    queryset = get_all_documents()
    paginate_by = 25


class DocumentByCategoryView(ListView):
    """ Класс вывода документов по выбранной категории. """
    
    template_name = 'bibliofund/documentsByCategory.html'
    context_object_name = 'documents'
    paginate_by = 25

    def get_queryset(self):
        self.queryset = get_documents_by_category(self.kwargs.get('category_name'))
        return super().get_queryset()


class DocumentDetailView(DetailView):
    """ Класс вывода подробной информации одного документа. """
    
    template_name = 'bibliofund/documentDetail.html'
    model = Document
    context_object_name = 'document'
