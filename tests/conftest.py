import pytest
from django.apps import apps


@pytest.fixture()
def simple_user(db, django_user_model):
    UserModel = django_user_model

    return UserModel.objects.create_user(
        username='simple',
        password='Pa$$w0rd',
    )

@pytest.fixture()
def bookmark_list(db, simple_user):
    BookmarkModel = apps.get_model('bookmark', 'Bookmark')
    return BookmarkModel.objects.bulk_create([
        BookmarkModel(
            url='https://google.com/',
            user=simple_user,
        ),
        BookmarkModel(
            url='https://gazeta.ru/',
            user=simple_user,
        )
    ])


@pytest.fixture(autouse=True, scope="function")
def _clear_django_cache():
    from django.core.cache import cache

    cache.clear()
