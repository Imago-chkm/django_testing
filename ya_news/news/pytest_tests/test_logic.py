from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError


@pytest.mark.django_db
def test_anonim_cant_create_comment(form_data, client, id_for_args):
    """Аноним не может отправить комментарий."""
    client.post(reverse(
        'news:detail',
        args=id_for_args
    ), data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_create_comment(form_data, author_client, id_for_args):
    """Авторизованный пользователь может отправить комментарий."""
    author_client.post(reverse(
        'news:detail',
        args=id_for_args
    ), data=form_data)
    assert Comment.objects.count() == 1


def test_user_cant_use_bad_words(author_client, id_for_args):
    """Нельзя отправлять запрещенные слова."""
    response = author_client.post(
        reverse('news:detail', args=id_for_args),
        data={'text': BAD_WORDS[0]}
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_his_comments(
    author_client,
    comment_id_for_args,
    form_data,
    comment
):
    """Автор может редактировать свои комментарии."""
    author_client.post(reverse(
        'news:edit',
        args=comment_id_for_args
    ), form_data)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_author_can_delete_his_comments(
    author_client,
    comment_id_for_args
):
    """Автор может удалять свои комментарии."""
    author_client.post(reverse('news:delete', args=comment_id_for_args))
    assert Comment.objects.count() == 0


def test_user_cant_edit_another_users_comments(
    not_author_client,
    comment_id_for_args,
    form_data,
    comment
):
    """Пользователь не может редактировать чужие комментарии."""
    assert not_author_client.post(reverse(
        'news:edit',
        args=comment_id_for_args
    ), form_data).status_code == HTTPStatus.NOT_FOUND
    assert comment.text == Comment.objects.get(id=comment.id).text


def test_user_cant_delele_another_users_comments(
    not_author_client,
    comment_id_for_args
):
    """Пользователь не может удалять чужие комментарии."""
    not_author_client.post(reverse('news:delete', args=comment_id_for_args))
    assert Comment.objects.count() == 1
