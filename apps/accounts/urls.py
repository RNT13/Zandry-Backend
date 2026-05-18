from django.urls import path

from apps.accounts.views.register_company_view import RegisterCompanyView
from .views.login_view import LoginView
from .views.logout_view import LogoutView
from .views.refresh_view import CookieTokenRefreshView
from .views.me_view import MeView

urlpatterns = [
    path("register-company/", RegisterCompanyView.as_view(), name="register-company"),

    path("login/",   LoginView.as_view(),           name="auth-login"),
    path("logout/",  LogoutView.as_view(),          name="auth-logout"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="auth-refresh"),
    path("me/",      MeView.as_view(),              name="auth-me"),
]
