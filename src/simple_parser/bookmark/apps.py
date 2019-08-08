from django.apps import AppConfig


class BookmarkConfig(AppConfig):
    name = 'simple_parser.bookmark'
    label = 'bookmark'
    verbose_name = 'Закладка'

    def ready(self):
        import simple_parser.bookmark.recievers
