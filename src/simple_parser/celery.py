import os
from celery import Celery
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_parser.settings.production')


app = Celery('simple_parser')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(related_name='celery_tasks')
