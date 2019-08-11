import logging

import requests
from celery.app import app_or_default
from django.conf import settings
from requests import RequestException

from simple_parser.core.contrib import parsing

from .models import Bookmark, EmbeddedMetadata

app = app_or_default()


@app.task(name='simple_parser.bookmark.parse_bookmark_url', queue='bookmark')
def parse_bookmark_url(bookmark_id, using=None):
    logger = logging.getLogger('simple_parser.bookmark.celery_tasks')

    bookmark = Bookmark.objects.get(id=bookmark_id)

    logger.info('Запрос html с сайта: {}'.format(bookmark.url))
    try:
        response = requests.get(bookmark.url)
    except RequestException:
        bookmark.is_available = False
        bookmark.save(update_fields=['is_available'])
        logger.warning('Не удалось получить html с сайта: {}'.format(bookmark.url))
        return

    logger.info('Запуск парсинга сайта {} с помощью парсера {}'.format(bookmark.url, using or getattr(settings, 'DEFAULT_PARSER', 'default')))
    parser = parsing.get_parser(response.text, bookmark.url, using=using)
    parser.parse()

    logger.info('Сайт: "{}". Title: "{}"; Description: "{}"; Favicon: "{}"'.format(
        bookmark.url,
        parser.title or '-не найдено-',
        parser.description or '-не найдено-',
        parser.favicon_url or '-не найдено-',
    ))
    EmbeddedMetadata.objects.create(
        type=using or getattr(settings, 'DEFAULT_PARSER', 'default'),
        title=parser.title or '-не найдено-',
        description=parser.description or '-не найдено-',
        favicon_url=parser.favicon_url or '-не найдено-',
        bookmark=bookmark,
    )
