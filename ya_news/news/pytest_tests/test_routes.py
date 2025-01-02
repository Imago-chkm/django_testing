from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('home_url'),
        lazy_fixture('detail_url'),
        lazy_fixture('login_url'),
        lazy_fixture('logout_url'),
        lazy_fixture('signup_url'),
    )
)
def test_pages_availability_for_anonymous_user(client, url):
    """Страницы, доступные анонимным пользователям."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('edit_url'),
        lazy_fixture('delete_url'),
    ),
)
def test_edit_delete_comments_availability_for_author(
    parametrized_client,
    url,
    expected_status
):
    """
    Страницы редактирования и удаления комментария доступны автору.
    Для анонима срабатывает ошибка 404.
    """
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('edit_url'),
        lazy_fixture('delete_url'),
    ),
)
def test_edit_delete_comments_redirect_for_anonim(client, login_url, url):
    """Редирект с редактирования и удаления комментария для анонима."""
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
