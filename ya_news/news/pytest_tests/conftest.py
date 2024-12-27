from datetime import datetime, timedelta
import pytest

from django.contrib.auth import get_user_model
from django.test.client import Client
from django.utils import timezone

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
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(constants.NEW_COUNT_FOR_PAGINATE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def create_comments(author, news):
    now = timezone.now()
    for index in range(2):
        comments = Comment.objects.create(
            news=news,
            text=index,
            author=author,
        )
        comments.created = now + timedelta(days=index)
        comments.save()
    return comments
