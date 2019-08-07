from .base import *  # noqa

# Django settings

DEBUG = True

SECRET_KEY = env('DJANGO_SECRET_KEY', default='xxxxxxxxxxxxxxxx')  # noqa

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])  # noqa

INTERNAL_IPS = env.list('DJANGO_INTERNAL_IPS', default=['127.0.0.1', '10.0.2.2'])

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/'


# Celery settings

CELERY_TASK_ALWAYS_EAGER = True


# Django Debug Toolbar settings

try:
    import debug_toolbar  # noqa
except ImportError:
    pass
else:
    INSTALLED_APPS += ['debug_toolbar']  # noqa

    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa

    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
        'SHOW_TEMPLATE_CONTEXT': True,
    }
