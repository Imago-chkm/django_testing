from datetime import datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News

from . import constants

User = get_user_model()


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def id_for_args(news):
    return news.id,
# пока что все ломается при попытке перенести в константы
# моих знаний не хватило, чтобы перенести это в константу,
# либо получается много кода вместо трех строк


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
def comment_id_for_args(comment):
    return comment.id,


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
    today = datetime.today()
    return News.objects.bulk_create(
        (News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        ) for index in range(constants.NEW_COUNT_FOR_PAGINATE + 1))
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
def home_url(client):
    return client.get(reverse('news:home'))


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=[news.id,])


@pytest.fixture
def edit_url(comment_id_for_args):
    return reverse(
        'news:edit',
        args=comment_id_for_args
    )


@pytest.fixture
def delete_url(comment_id_for_args):
    return reverse('news:delete', args=comment_id_for_args)


@pytest.fixture
def empty_comment_in_db():
    return Comment.objects.all().delete()
