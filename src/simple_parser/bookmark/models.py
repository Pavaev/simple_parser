from django.conf import settings
from django.db import models
from enumfields import EnumField

from .constants import EmbeddedMetadataTypes


class Bookmark(models.Model):
    url = models.URLField(
        'адрес сайта',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        related_name='bookmarks',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        'дата создания',
        auto_now_add=True,
    )
    is_available = models.BooleanField(
        'сайт доступен',
        default=True,
    )

    class Meta:
        verbose_name = 'закладка'
        verbose_name_plural = 'закладки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'url'],
                name='unique_user_bookmark_url',
            ),
        ]

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        return self.url

    def __repr__(self):
        return '<{}: id={}, url={}, user_id={}, date_created={}, is_available={}>'.format(
            self.__class__.__name__, self.id, self.url, self.user_id,
            self.date_created, self.is_available,
        )


# Для расширяемости вынесено в отдельную модель. Например, если будет
# необходимо хранить метаданные сразу нескольких типов для закладки
class EmbeddedMetadata(models.Model):
    type = EnumField(
        EmbeddedMetadataTypes,
        verbose_name='тип',
        max_length=10,
    )
    title = models.TextField(
        'заголовок',
        blank=True,
    )
    description = models.TextField(
        'описание',
        blank=True,
    )
    favicon_url = models.URLField(
        'URL favicon',
        blank=True,
    )
    bookmark = models.OneToOneField(
        'Bookmark',
        verbose_name='закладка',
        related_name='embedded_metadata',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        'дата создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'встроенные метаданные'
        verbose_name_plural = 'встроенные метаданные'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['bookmark', 'type'],
        #         name='unique_bookmark_embedded_metadata_type',
        #     ),
        # ]

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        return 'Тип: {}; Заголовок: {}; Описание: {}; Favicon: {}'.format(
            self.type.label,
            self.title or '-не найдено-',
            self.description or '-не найдено-',
            self.favicon_url or '-не найдено-',
        )

    def __repr__(self):
        return '<{}: id={}, type={}, title={}, description={}, favicon_url={}, bookmark_id={}, date_created={}>'.format(
            self.__class__.__name__, self.id, self.type, self.title,
            self.description, self.favicon_url, self.bookmark_id,
            self.date_created,
        )
