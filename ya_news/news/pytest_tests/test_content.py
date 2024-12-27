import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture

from . import constants


@pytest.mark.django_db
def test_homepage_paginate_10(all_news, client):
    """Количество новостей на главной странице — не более 10."""
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    assert len(object_list) == constants.NEW_COUNT_FOR_PAGINATE


@pytest.mark.django_db
def test_news_order_by_pub_date(all_news, client):
    """Сортировка новостей от новых к старым."""
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order_by_pub_date(client, create_comments, id_for_args):
    """Сортировка комментариев от новых к старым."""
    response = client.get(reverse('news:detail', args=id_for_args))
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert 'news' in response.context
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrize_client, expecting_answer',
    (
        (lazy_fixture('auth_client'), True),
        (lazy_fixture('client'), False),
    )
)
def test_comment_form_availability_for_auth_users(
    id_for_args,
    parametrize_client,
    expecting_answer
):
    """Форма комментариев доступна только авторизованным."""
    response = parametrize_client.get(reverse('news:detail', args=id_for_args))
    if expecting_answer is True:
        assert 'form' in response.context
    else:
        assert 'form' not in response.context
