from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.encoding import force_bytes

UserModel = get_user_model()


def test_invalid_login(client, simple_user):
    data = {
        'username': 'simple',
        'password': 'xxxxxxxx',
    }

    response = client.post(
        reverse('login'), data=data, follow=True,
    )

    assert response.status_code == 200
    assert auth.SESSION_KEY not in client.session
    assert auth.BACKEND_SESSION_KEY not in client.session


def test_valid_login(client, simple_user):
    data = {
        'username': 'simple',
        'password': 'Pa$$w0rd',
    }

    response = client.post(
        reverse('login'), data=data, follow=True,
    )

    assert response.status_code == 200
    assert str(simple_user.id) == client.session.get(auth.SESSION_KEY)


def test_redirect_after_login(settings, client, simple_user):
    data = {
        'username': 'simple',
        'password': 'Pa$$w0rd',
    }

    response = client.post(
        reverse('login'), data=data, follow=True,
    )
    assert len(response.redirect_chain) == 1
    assert response.redirect_chain[0][0] == resolve_url(settings.LOGIN_REDIRECT_URL)


def test_redirect_after_logout(settings, client, simple_user):
    client.login(username='simple', password='Pa$$w0rd')

    response = client.post(reverse('logout'), follow=True)
    assert len(response.redirect_chain) == 1
    assert response.redirect_chain[0][0] == resolve_url(settings.LOGIN_URL)


def test_redirect_already_authorized(settings, client, simple_user):
    client.login(username='simple', password='Pa$$w0rd')

    response = client.get(reverse('login'), follow=True)
    assert len(response.redirect_chain) == 1
    assert response.redirect_chain[0][0] == resolve_url(settings.LOGIN_REDIRECT_URL)


def test_duplicate_username_registration(client, simple_user):
    data = {
        'username': 'simple',
        'password1': 'Pa$$w0rd',
        'password2': 'Pa$$w0rd',
    }
    response = client.post(reverse('register'), data=data, follow=True)

    assert response.status_code == 200
    assert force_bytes('Пользователь с таким именем уже существует') in response.content


def test_registration(client, db):
    password = UserModel.objects.make_random_password()
    data = {
        'username': 'new-user',
        'password1': password,
        'password2': password,
    }
    response = client.post(reverse('register'), data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == resolve_url(settings.LOGIN_REDIRECT_URL)
    assert UserModel.objects.filter(username='new-user').exists()
