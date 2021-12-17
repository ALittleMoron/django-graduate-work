from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path

from .views import HomePageView, UserAccountView, UserLoginView, UserRegisterView

urlpatterns = [
    path('', HomePageView.as_view(), name='graduateWork/homePage'),
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
    
]
