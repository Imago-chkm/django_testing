import pytest

from django.urls import reverse

from . import constants


@pytest.mark.django_db
def test_homepage_paginate_10(news_for_paginate, client):
    """Количество новостей на главной странице — не более 10."""
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    assert len(object_list) == constants.NEW_COUNT_FOR_PAGINATE

# def test_news_order_by_pub_date():
#     """Сортировка новостей от новых к старым."""
#     pass

# def test_comments_order_by_pub_date():
#     """Сортировка комментариев от новых к старым."""
#     pass

# def test_comment_form_availability_for_auth_users():
#     """Форма комментариев доступна только авторизованным."""
#     pass