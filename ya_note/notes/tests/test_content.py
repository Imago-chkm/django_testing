from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
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
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.url_list = reverse('notes:list')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author
        )

    def test_note_passed_with_list_notes(self):
        """Заметка передаётся на страницу со списком заметок."""
        response = self.author_client.get(self.url_list)
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_list_only_author(self):
        """В список заметок одного пользователя не попадают заметки другого."""
        response = self.reader_client.get(self.url_list)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_forms_in_add_and_delete_pages(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            url = reverse(name, args=args)
            response = self.author_client.get(url)
            self.assertIn('form', response.context)
