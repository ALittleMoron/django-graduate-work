from typing import Any, Dict, Union

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView, ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm, DocumentForm
from .mixins import UserIsPublisher
from .models import Document
from .services import (get_all_documents, get_documents_by_category, get_documents_by_user,
                       get_searched_documents_by_param)


class UserAccountView(ListView):
    """ Класс обработки работы с аккаунтом пользователя. 
    
    Унаследован от ListView для того, чтобы было удобно выводить все документы пользователя.
    """

    template_name = 'bibliofund/account.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['author'] = self.queryset[0].publisher
        return context
    
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
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        self.queryset = get_documents_by_category(self.kwargs['slug'])
        return super().get_queryset()


class DocumentDetailView(DetailView):
    """ Класс вывода подробной информации одного документа. """
    
    template_name = 'bibliofund/documentDetail.html'
    model = Document
    context_object_name = 'document'
    slug_url_kwarg = 'slug'
    


class SearchResultView(ListView):
    """ Класс вывода документов из поиска по названию. """

    template_name = 'bibliofund/searchResult.html'
    context_object_name = 'documents'
    paginate_by = 18
    
    def get_queryset(self):
        search_param = self.request.GET.get('param')
        self.queryset = get_searched_documents_by_param(search_param)
        return super().get_queryset()


class AddDocumentView(LoginRequiredMixin, CreateView):
    """  """
    form_class = DocumentForm
    template_name = ''
    
    def form_valid(self, form: DocumentForm) -> HttpResponseRedirect:
        """ Переопределенный метод класса CreateView для добавление автора
        на этапе, когда форма провалидировалась. 
        """
        form.instance.publisher = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.object.get_absolute_url())
    
    def post(self, request, *args, **kwargs):
        """ Переопределенный метод клааса CreateView для отправки сообщения об
        ошибки валидации формы.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DucumentDetailView(DetailView):
    """ Класс отображения подробной информации о картинке. """
    model = Document
    template_name = ""
    context_object_name = ''


class DocumentUpdateView(LoginRequiredMixin, CreateView):
    """ """
    model = Document
    form_class = ...
    template_name = ''
    context_object_name = ''


class DocumentUpdateView(UserIsPublisher, UpdateView):
    """ """
    model = Document
    form_class = ...
    template_name = ''
    context_object_name = ''


class DocumentDeleteView(UserIsPublisher, DeleteView):
    """ """
    model = Document
    template_name = ''
    context_object_name = ''
    success_url = '/'