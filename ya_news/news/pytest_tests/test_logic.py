import pytest

from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment



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

    # def test_author_can_edit_his_comments(self):
    #     """Автор может редактировать свои комментарии."""
    #     pass

    # def test_author_can_delete_his_comments(self):
    #     """Автор может удалять свои комментарии."""
    #     pass

    # def test_user_cant_edit_another_users_comments(self):
    #     """Пользователь не может редактировать чужие комментарии."""
    #     pass

    # def test_user_cant_delele_another_users_comments(self):
    #     """Пользователь не может удалять чужие комментарии."""
    # pass
