from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.url_add = reverse('notes:add')
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
        }
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author
        )

    def test_anonim_cant_create_note(self):
        """Аноним не может создавать заметки."""
        self.client.post(self.url_add, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    # def test_logged_user_can_create_note(self):
    #     """Залогиненый юзер может создавать заметки."""
    #     pass

    # def test_no_possible_two_same_slug(self):
    #     """Невозможно создать две заметки с одинаковым slug."""
    #     pass

    # def test_automatic_slug_generation(self):
    #     """slug формируется автоматически, если не был заполнен."""
    #     pass

    # def test_author_can_edit_his_notes(self):
    #     """Автор может редактировать свои заметки."""
    #     pass

    # def test_author_can_delete_his_notes(self):
    #     """Автор может удалять свои заметки."""
    #     pass

    # def test_user_cant_edit_another_users_notes(self):
    #     """Пользователь не может редактировать чужие заметки."""
    #     pass

    # def test_user_cant_delele_another_users_notes(self):
    #     """Пользователь не может удалять чужие заметки."""
    #     pass
