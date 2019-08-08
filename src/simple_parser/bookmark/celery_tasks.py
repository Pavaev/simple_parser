import requests
from celery.app import app_or_default
from django.conf import settings
from requests import RequestException

from simple_parser.core.contrib import parsing

from .models import Bookmark, EmbeddedMetadata

app = app_or_default()


@app.task(name='simple_parser.bookmark.parse_bookmark_url', queue='bookmark')
def parse_bookmark_url(bookmark_id, using=None):
    bookmark = Bookmark.objects.get(id=bookmark_id)

    try:
        response = requests.get(bookmark.url)
    except RequestException:
        bookmark.is_available = False
        bookmark.save(update_fields=['is_available'])
        return

    parser = parsing.get_parser(response.text, bookmark.url, using=using)
    parser.parse()

    EmbeddedMetadata.objects.create(
        type=using or getattr(settings, 'DEFAULT_PARSER', 'default'),
        title=parser.title or '',
        description=parser.description or '',
        favicon_url=parser.favicon_url or '',
        bookmark=bookmark,
    )
