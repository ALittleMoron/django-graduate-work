from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path

from .views import (AllDocumentsView, DocumentByCategoryView, DocumentDetailView,
                    DocumentUpdateView, HomePageView, UserAccountView, UserLoginView,
                    UserRegisterView, SearchResultView)

urlpatterns = [
    path('', HomePageView.as_view(), name='graduateWork/homePage'),
    path('search', SearchResultView.as_view(), name='graduateWork/searchResult'),
    path('account/<str:username>', UserAccountView.as_view(), name='graduateWork/account'),
    path('account/auth/login', UserLoginView.as_view(), name='graduateWork/login'),
    path('account/auth/registration', UserRegisterView.as_view(), name='graduateWork/registration'),
    # path('account/change_password')
    path(
        'account/auth/logout',
        LogoutView.as_view(),
        {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='graduateWork/logout'
    ),
    path('all-documents', AllDocumentsView.as_view(), name='graduateWork/allDocuments'),
    path(
        'documents-by-category/<slug:slug>',
        DocumentByCategoryView.as_view(),
        name='graduateWork/documentsByCategory'
    ),
    path('document/<slug:slug>', DocumentDetailView.as_view(), name='graduateWork/documentDetail'),
    path('create-document', DocumentUpdateView.as_view(), name='graduateWork/documentCreate'),
]
