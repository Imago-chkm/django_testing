from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News

FORM_DATA = {'text': 'Comment'}

User = get_user_model()


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        text='Tекст',
        author=author,
    )


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def all_news():
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def auth_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=[news.id, ])


@pytest.fixture
def edit_url(comment):
    return reverse(
        'news:edit',
        args=[comment.id, ]
    )


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=[comment.id, ])


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
