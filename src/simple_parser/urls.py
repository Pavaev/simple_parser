from django.conf import settings
from django.urls import path, include

urlpatterns = []

# Auth
from simple_parser.auth.urls import urlpatterns as auth_urlpatterns
urlpatterns += auth_urlpatterns

# Parsing
from simple_parser.parsing.urls import urlpatterns as parsing_urlpatterns
urlpatterns += parsing_urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static  # noqa

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar  # noqa

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns