from .production import *

DEBUG = False

SECRET_KEY = env('DJANGO_SECRET_KEY', default='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

AXES_ENABLED = False

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
