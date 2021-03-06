# Generated by Django 2.2.4 on 2019-08-13 07:35

import django.db.models.deletion
import enumfields.fields
from django.conf import settings
from django.db import migrations, models

import simple_parser.bookmark.constants


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500, verbose_name='адрес сайта')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('is_available', models.BooleanField(default=True, verbose_name='сайт доступен')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'закладка',
                'verbose_name_plural': 'закладки',
            },
        ),
        migrations.CreateModel(
            name='EmbeddedMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', enumfields.fields.EnumField(enum=simple_parser.bookmark.constants.EmbeddedMetadataTypes, max_length=10, verbose_name='тип')),
                ('title', models.TextField(blank=True, verbose_name='заголовок')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('favicon_url', models.URLField(blank=True, max_length=500, verbose_name='URL favicon')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('bookmark', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='embedded_metadata', to='bookmark.Bookmark', verbose_name='закладка')),
            ],
            options={
                'verbose_name': 'встроенные метаданные',
                'verbose_name_plural': 'встроенные метаданные',
            },
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(fields=('user', 'url'), name='unique_user_bookmark_url'),
        ),
    ]
