from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', lazy_fixture('id_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    """Страницы, доступные анонимным пользователям."""
    url = reverse(name, args=args)
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
    'name, args',
    (
        ('news:edit', lazy_fixture('comment_id_for_args')),
        ('news:delete', lazy_fixture('comment_id_for_args')),
    ),
)
def test_edit_delete_comments_availability_for_author(
    parametrized_client,
    name,
    args,
    expected_status
):
    """Страницы редактирования и удаления комментария доступны автору."""
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

# def test_edit_delete_comments_redirect_for_anonim():
#     """Редирект с редактирования и удаления комментария для анонима."""
#     pass

# def test_edit_delete_comments_404_for_another_users():
#     """Ошибка 404 для юзеров касаемо чужих комментариев."""
#     pass
