from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from . import conftest


@pytest.mark.django_db
def test_anonim_cant_create_comment(client, detail_url):
    """Аноним не может отправить комментарий."""
    Comment.objects.all().delete()
    client.post(detail_url, data=conftest.FORM_DATA)
    assert Comment.objects.first() is None


@pytest.mark.django_db
def test_auth_user_can_create_comment(
    author_client,
    detail_url
):
    """Авторизованный пользователь может отправить комментарий."""
    Comment.objects.all().delete()
    author_client.post(detail_url, data=conftest.FORM_DATA)
    assert Comment.objects.first()


def test_user_cant_use_bad_words(
    author_client,
    detail_url
):
    """Нельзя отправлять запрещенные слова."""
    Comment.objects.all().delete()
    response = author_client.post(
        detail_url,
        data={'text': BAD_WORDS[0]}
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.first() is None


def test_author_can_edit_his_comments(
    author_client,
    edit_url,
    comment
):
    """Автор может редактировать свои комментарии."""
    author_client.post(edit_url, conftest.FORM_DATA)
    edited_comment = Comment.objects.get(id=comment.id)
    assert edited_comment.text == conftest.FORM_DATA['text']


def test_author_can_delete_his_comments(
    author_client,
    delete_url
):
    """Автор может удалять свои комментарии."""
    initial_comment_count = Comment.objects.count()
    author_client.post(delete_url)
    assert Comment.objects.first() is None
    assert initial_comment_count != Comment.objects.count()


def test_user_cant_edit_another_users_comments(
    not_author_client,
    edit_url,
    comment
):
    """Пользователь не может редактировать чужие комментарии."""
    initial_comments = list(Comment.objects.all())
    assert not_author_client.post(
        edit_url,
        conftest.FORM_DATA
    ).status_code == HTTPStatus.NOT_FOUND
    final_comments = list(Comment.objects.all())
    assert len(set(initial_comments) - set(final_comments)) == 0
    assert comment.text == Comment.objects.get(id=comment.id).text


def test_user_cant_delele_another_users_comments(
    not_author_client,
    delete_url
):
    """Пользователь не может удалять чужие комментарии."""
    not_author_client.post(delete_url)
    assert Comment.objects.count() == 1
