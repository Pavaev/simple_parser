from pathlib import Path

import environ

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# Utilities

APP_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = APP_DIR.parent.parent

env_file = APP_DIR.joinpath('../.env')
if env_file.exists():
    print('Loading .env file...'.format(env_file))
    env.read_env(str(env_file))

DATA_DIR = env.get_value('SIMPLE_PARSER_DATA_DIR', cast=Path, default=BASE_DIR.joinpath('data'))
if not DATA_DIR.exists():
    DATA_DIR.mkdir()

LOGS_DIR = env.get_value('SIMPLE_PARSER_LOGS_DIR', cast=Path, default=BASE_DIR.joinpath('logs'))
if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()

# Django settings

DEBUG = env.bool('DJANGO_DEBUG', False)

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

THIRD_PARTY_APPS = [
    'axes',
    'captcha',
    'bootstrap3',
]

LOCAL_APPS = [
    'simple_parser.account',
    'simple_parser.bookmark',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # It only formats user lockout messages and renders Axes lockout responses
    # on failed user authentication attempts from login views.
    # If you do not want Axes to override the authentication response
    # you can skip installing the middleware and use your own views.
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'simple_parser.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APP_DIR.joinpath('templates')),
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simple_parser.wsgi.application'


# Database

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL', default='postgres:///simple_parser'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = str(DATA_DIR.joinpath('static'))
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(APP_DIR.joinpath('static')),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'simple_parser': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'django.server': {
            'level': 'INFO',
            'handlers': ['django.server'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# Axes
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_URL = '/locked'


# Parsing
DEFAULT_PARSER = env.str('DEFAULT_PARSER', default='default')

# Celery settings

from kombu import Queue  # noqa


CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
CELERY_BROKER_TRANSPORT_OPTIONS = {}

CELERY_RESULT_BACKEND = None
CELERY_RESULT_EXPIRES = 1
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_SEND_EVENTS = False

CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_WORKER_REDIRECT_STDOUTS = False
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# Ensure workers run async by default
# in Development you might want them to     run in-process
# though it would cause timeouts/recursions in some cases
CELERY_TASK_ALWAYS_EAGER = False

CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_SERIALIZER = 'json'

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

CELERY_TASK_QUEUES = [
    Queue('default', routing_key='default'),
    Queue('bookmark', routing_key='bookmark'),
]

try:
    import django_heroku
except ImportError:
    pass
else:
    django_heroku.settings(locals())
