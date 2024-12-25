from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()

NOTES_COUNT_ON_HOME_PAGE = 10


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author
        )

    # def test_note_passed_with_list_notes(self):
    #     """Отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context."""
    #     pass

    # def test_notes_list_only_author(self):
    #     """В список заметок одного пользователя не попадают заметки другого пользователя."""
    #     pass

    # def test_forms_in_add_and_delete_pages(self):
    #     """На страницы создания и редактирования заметки передаются формы."""
    #     pass
