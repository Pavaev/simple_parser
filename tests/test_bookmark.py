from django.urls import reverse
from django.utils.encoding import force_bytes


def test_invalid_url_addition(client, simple_user):
    client.force_login(simple_user)

    data = {
        'url': 'xxx'
    }

    response = client.post(reverse('create-bookmark'), follow=True, data=data)

    assert response.status_code == 200
    assert force_bytes('Введите правильный URL.') in response.content


def test_valid_url_addition(client, simple_user):
    client.force_login(simple_user)

    data = {
        'url': 'https://google.com'
    }

    response = client.post(reverse('create-bookmark'), follow=True, data=data)

    assert response.status_code == 200
    assert force_bytes('Данный урл уже был добавлен') not in response.content


def test_duplicate_url_addition(client, simple_user, bookmark_list):
    client.force_login(simple_user)

    data = {
        'url': 'https://google.com'
    }

    response = client.post(reverse('create-bookmark'), follow=True, data=data)

    assert response.status_code == 200
    assert force_bytes('Данный урл уже был добавлен') in response.content