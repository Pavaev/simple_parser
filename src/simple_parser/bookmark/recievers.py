from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(signal=post_save, sender='bookmark.Bookmark', dispatch_uid='queue_bookmark_for_parsing')
def queue_bookmark_for_parsing(instance, created, **kwargs):
    from simple_parser.bookmark.celery_tasks import parse_bookmark_url

    # На данный момент не рассматриваются повторные проверки
    if not created:
        return
    transaction.on_commit(lambda: parse_bookmark_url.delay(instance.id))
