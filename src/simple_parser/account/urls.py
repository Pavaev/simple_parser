from axes.decorators import axes_dispatch
from django.contrib.auth import views
from django.urls import include, path
from django.utils.decorators import method_decorator

from simple_parser.core.contrib.auth.decorators import logout_or_404

from .views import captcha_view, register_view

urlpatterns = [
    path('captcha', include('captcha.urls')),

    path(
        'login',
        method_decorator(axes_dispatch, name='dispatch')(views.LoginView).as_view(
            template_name='account/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path(
        'logout',
        views.logout_then_login,
        name='logout',
    ),
    path('register', logout_or_404(register_view), name='register'),
    path('locked', logout_or_404(captcha_view), name='locked')
]
