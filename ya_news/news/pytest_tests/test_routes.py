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

# def test_edit_delete_comments_availability_for_author():
#     """Страницы редактирования и удаления комментария доступны автору."""
#     pass

# def test_edit_delete_comments_redirect_for_anonim():
#     """Редирект с редактирования и удаления комментария для анонима."""
#     pass

# def test_edit_delete_comments_404_for_another_users():
#     """Ошибка 404 для юзеров касаемо чужих комментариев."""
#     pass
