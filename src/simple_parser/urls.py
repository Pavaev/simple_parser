from django.conf import settings
from django.urls import path, include

urlpatterns = []

# Auth
from simple_parser.account.urls import urlpatterns as auth_urlpatterns
urlpatterns += auth_urlpatterns

# Bookmark
from simple_parser.bookmark.urls import urlpatterns as bookmark_urlpatterns
urlpatterns += bookmark_urlpatterns


if settings.DEBUG:
    from django.conf.urls.static import static  # noqa

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar  # noqa

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns