from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path

from .views import HomePage, UserAccountView, UserLoginView, UserRegisterView

urlpatterns = [
    path('', HomePage.as_view(), name='graduateWork/homePage'),
    path('account/<str:username>', UserAccountView.as_view(), name='graduateWork/account'),
    path('account/login', UserLoginView.as_view(), name='graduateWork/login'),
    path('account/registration', UserRegisterView.as_view(), name='graduateWork/registration'),
    # path('account/change_password')
    path(
        'logout',
        LogoutView.as_view(),
        {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='graduateWork/logout'
    ),
    
]
