import pytest


@pytest.fixture()
def simple_user(db, django_user_model):
    UserModel = django_user_model

    return UserModel.objects.create_user(
        username='simple',
        password='Pa$$w0rd',
    )


@pytest.fixture(autouse=True, scope="function")
def _clear_django_cache():
    from django.core.cache import cache

    cache.clear()
