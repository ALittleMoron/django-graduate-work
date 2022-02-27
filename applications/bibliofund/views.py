from typing import Any, Dict, Union
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpRequest, FileResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView, ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

from .forms import (CustomAuthenticationForm, CustomUserCreationForm, DocumentForm,
                    DocumentUpdateForm)
from .mixins import UserIsPublisher
from .models import Document, FileStatistic
from .services import (get_all_documents, get_document, get_documents_by_category,
                       get_documents_by_user, get_searched_documents_by_param)


class Download(View):
    def get(self, request, *args, **kwargs):
        file_name = self.kwargs.get('file_name')
        username = self.kwargs.get('username')
        file_path = os.path.join(settings.BASE_DIR, 'media', 'documents', f'user_{username}', file_name)
        if os.path.exists(file_path):
            file_filter_path = os.path.join('documents', f'user_{username}', file_name)
            stat = Document.objects.get(file=file_filter_path).statistic
            stat.increment_field('download_count')
            return FileResponse(open(file_path, 'rb'))
        raise Http404


class UserAccountView(ListView):
    """ Класс обработки работы с аккаунтом пользователя. 
    
    Унаследован от ListView для того, чтобы было удобно выводить все документы пользователя.
    """

    template_name = 'bibliofund/account.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['author'] = get_user_model().objects.get(username=self.kwargs.get('username'))
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


class AllDocumentsBaseView(ListView):
    """ Базовый класс вывода всех опубликованных документов """
    template_name = 'bibliofund/documents.html'
    context_object_name = 'documents'
    paginate_by = 25

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все документы'
        return context

class AllDocumentsView(AllDocumentsBaseView):
    """ Класс вывода всех опубликованных документов. """
    queryset = get_all_documents(order_by='?')


class NewestDocumentsView(AllDocumentsBaseView):
    """ Класс вывода новейших документов """
    queryset = get_all_documents(order_by='-updated_at')


class RelevantDocumentsView(AllDocumentsBaseView):
    """ Класс вывода релевантных документов """
    queryset = get_all_documents(order_by='-statistic__download_count')


class DocumentByCategoryView(ListView):
    """ Класс вывода документов по выбранной категории. """
    
    template_name = 'bibliofund/documents.html'
    context_object_name = 'documents'
    paginate_by = 25
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Документы по категории'
        return context

    def get_queryset(self):
        self.queryset = get_documents_by_category(self.kwargs['slug'])
        return super().get_queryset()


class SearchResultView(ListView):
    """ Класс вывода документов из поиска по названию. """

    template_name = 'bibliofund/searchResult.html'
    context_object_name = 'documents'
    paginate_by = 18
    
    def get_queryset(self):
        search_param = self.request.GET.get('param')
        self.queryset = get_searched_documents_by_param(search_param)
        return super().get_queryset()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        return context


class DocumentCreateView(LoginRequiredMixin, CreateView):
    """  """
    form_class = DocumentForm
    template_name = 'bibliofund/documentForm.html'
    
    def form_valid(self, form: DocumentForm) -> HttpResponseRedirect:
        """ Переопределенный метод класса CreateView для добавление автора
        на этапе, когда форма провалидировалась. 
        """
        form.instance.publisher = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class DocumentDetailView(DetailView):
    """ Класс вывода подробной информации одного документа. """
    
    template_name = 'bibliofund/documentDetail.html'
    model = Document
    context_object_name = 'document'
    slug_url_kwarg = 'slug'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.statistic = FileStatistic.objects.get(document=self.object)
        self.statistic.increment_field('view_count')
        self.statistic.refresh_from_db()
        context = self.get_context_data(object=self.object, statistic=self.statistic)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Документ'
        return context
    
    def get_queryset(self):
        self.queryset = get_document(self.kwargs['slug'])
        return super().get_queryset()


class DocumentUpdateView(UserIsPublisher, UpdateView):
    """ """
    model = Document
    form_class = DocumentUpdateForm
    template_name = 'bibliofund/documentForm.html'
    context_object_name = 'document'


class DocumentDeleteView(UserIsPublisher, DeleteView):
    """ """
    model = Document
    template_name = 'bibliofund/documentDelete.html'
    context_object_name = 'document'
    success_url = '/'
