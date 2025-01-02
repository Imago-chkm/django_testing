import pytest

from news.forms import CommentForm
from yanews import settings

pytestmark = pytest.mark.django_db


def test_homepage_paginate(all_news, home_url, client):
    """Количество новостей на главной странице — не более установленного."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order_by_pub_date(all_news, home_url, client):
    """Сортировка новостей от новых к старым."""
    response = client.get(home_url)
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


def test_comment_form_availability_for_auth_users(
    detail_url,
    auth_client
):
    """Форма комментариев доступна только авторизованным."""
    response = auth_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_comment_form_not_availability_for_anonim(
    detail_url,
    client
):
    """Форма комментариев недоступна анонимам."""
    response = client.get(detail_url)
    assert 'form' not in response.context
