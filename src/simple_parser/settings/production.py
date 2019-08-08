from .base import *  # noqa

# Django settings

DEBUG = False

SECRET_KEY = env('DJANGO_SECRET_KEY')  # noqa

DATABASES['default'] = env.db('DJANGO_DATABASE_URL')  # noqa

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379'),  # noqa
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# MIDDLEWARE.insert(0, 'django.middleware.security.SecurityMiddleware')  # noqa
#
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_FRAME_DENY = True
# SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)  # noqa
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
#
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])  # noqa

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/'

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

LOGGING['handlers']['console'] = {  # noqa
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'verbose',
}

# Celery settings

CELERY_BROKER_URL = env('CELERY_BROKER_URL')  # noqa
