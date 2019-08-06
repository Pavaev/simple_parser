from django.conf import settings
from django.contrib.auth import views
from django.urls import path, include

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

]

# Parsing
from simple_parser.parsing.urls import urlpatterns as parsing_urlpatterns
urlpatterns += parsing_urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static  # noqa

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar  # noqa

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns