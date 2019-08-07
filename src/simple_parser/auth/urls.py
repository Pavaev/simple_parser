from django.contrib.auth import views
from django.urls import path

from simple_parser.core.contrib.auth.decorators import logout_or_404

from .views import register_view

urlpatterns = [
    path(
        'login',
        views.LoginView.as_view(
            template_name='auth/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path(
        'logout',
        views.logout_then_login,
        name='logout',
    ),
    path('register', logout_or_404(register_view), name='register')
]
