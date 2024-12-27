import pytest

from django.contrib.auth import get_user_model

from news.models import News


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def id_for_args(news):
    return news.id,
