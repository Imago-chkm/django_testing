import pytest
from pytest_lazyfixture import lazy_fixture

from . import constants

pytestmark = pytest.mark.django_db


def test_homepage_paginate(all_news, home_url):
    """Количество новостей на главной странице — не более установленного."""
    response = home_url
    object_list = response.context['object_list']
    assert object_list.count() == constants.NEW_COUNT_FOR_PAGINATE


def test_news_order_by_pub_date(all_news, home_url):
    """Сортировка новостей от новых к старым."""
    response = home_url
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order_by_pub_date(detail_url, client):
    """Сортировка комментариев от новых к старым."""
    response = client.get(detail_url)
    news = response.context['news']
    news_comments = news.comment_set.all()
    all_comments = [comment.created for comment in news_comments]
    sorted_comments = sorted(all_comments)
    assert 'news' in response.context
    assert all_comments == sorted_comments


@pytest.mark.parametrize(
    'parametrize_client, expecting_answer',
    (
        (lazy_fixture('auth_client'), True),
    )
)
def test_comment_form_availability_for_auth_users(
    detail_url,
    parametrize_client,
    expecting_answer
):
    """Форма комментариев доступна только авторизованным."""
    response = parametrize_client.get(detail_url)
    assert 'form' in response.context


@pytest.mark.parametrize(
    'parametrize_client, expecting_answer',
    (
        (lazy_fixture('client'), False),
    )
)
def test_comment_form_not_availability_for_anonim(
    detail_url,
    parametrize_client,
    expecting_answer
):
    """Форма комментариев недоступна анонимам."""
    response = parametrize_client.get(detail_url)
    assert 'form' not in response.context
