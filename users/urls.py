from django.contrib.auth import views as auth_views
from django.urls import path

from core.ratelimit import rate_limit

from . import views
from .forms import EmailAuthenticationForm

urlpatterns = [
    path('register/', rate_limit('register', max_attempts=10, window_seconds=3600)(views.register), name='register'),
    path('login/', rate_limit('login', max_attempts=10, window_seconds=300)(auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=EmailAuthenticationForm,
        redirect_authenticated_user=True,
    )), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
