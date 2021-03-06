from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path

from .views import (Download, AllDocumentsView, DocumentByCategoryView, DocumentCreateView,
                    DocumentDeleteView, DocumentDetailView,DocumentUpdateView, NewestDocumentsView, RelevantDocumentsView, UserAccountView,
                    UserLoginView, UserRegisterView, SearchResultView)

urlpatterns = [
    path('', AllDocumentsView.as_view(), name='graduateWork/homePage'),
    path('newest-documents', NewestDocumentsView.as_view(), name='graduateWork/newestDocuments'),
    path('relevant-documents', RelevantDocumentsView.as_view(), name='graduateWork/relevantDocuments'),
    path('download/<str:username>/<str:file_name>', Download.as_view(), name='graduateWork/download'),
    path('search', SearchResultView.as_view(), name='graduateWork/searchResult'),
    path('account/<str:username>', UserAccountView.as_view(), name='graduateWork/account'),
    path('account/auth/login', UserLoginView.as_view(), name='graduateWork/login'),
    path('account/auth/registration', UserRegisterView.as_view(), name='graduateWork/registration'),
    path(
        'account/auth/logout',
        LogoutView.as_view(),
        {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='graduateWork/logout'
    ),
    path(
        'documents-by-category/<slug:slug>',
        DocumentByCategoryView.as_view(),
        name='graduateWork/documentsByCategory'
    ),
    path('document/create', DocumentCreateView.as_view(), name='graduateWork/documentCreate'),
    path('document/<slug:slug>', DocumentDetailView.as_view(), name='graduateWork/documentDetail'),
    path(
        'document/<slug:slug>/update',
        DocumentUpdateView.as_view(),
        name='graduateWork/documentUpdate'
    ),
    path(
        'document/<slug:slug>/delete',
        DocumentDeleteView.as_view(),
        name='graduateWork/documentDelete'
    ),
]
