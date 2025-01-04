from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class Fixtures(TestCase):
    """Общие текстуры для остальных тестовых файлов."""

    SLUG_TITLE = 'title'
    SLUG_CHECK = 'slug check'
    NOTE_TEXT = 'заметка'
    NEW_NOTE_TEXT = 'обновленная заметка'
    URL_NOTES_ADD = 'notes:add'
    URL_NOTES_SUCCESS = 'notes:success'
    URL_NOTES_LIST = 'notes:list'
    URL_NOTES_EDIT = 'notes:edit'
    URL_NOTES_DELETE = 'notes:delete'
    URL_NOTES_DETAIL = 'notes:detail'
    URL_LOGIN = reverse('users:login')
    PUBLIC_URLS = (
        ('notes:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
    FOR_AUTH_URLS = (
        URL_NOTES_LIST,
        URL_NOTES_ADD,
        URL_NOTES_SUCCESS
    )
    PRIVATE_AUTH_URLS = (
        URL_NOTES_EDIT,
        URL_NOTES_DELETE,
        URL_NOTES_DETAIL
    )

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text=cls.NOTE_TEXT,
            slug=cls.SLUG_TITLE,
            author=cls.author
        )
        cls.url_add = reverse(cls.URL_NOTES_ADD)
        cls.url_edit = reverse(cls.URL_NOTES_EDIT, args=(cls.note.slug,))
        cls.url_delete = reverse(cls.URL_NOTES_DELETE, args=(cls.note.slug,))
        cls.url_success = reverse(cls.URL_NOTES_SUCCESS)
        cls.url_list = reverse(cls.URL_NOTES_LIST)
        cls.form_data = {
            'title': cls.SLUG_CHECK,
            'text': cls.NEW_NOTE_TEXT,
        }

    def get_redirect_urls_data(self):
        return (
            (self.URL_NOTES_LIST, None),
            (self.URL_NOTES_SUCCESS, None),
            (self.URL_NOTES_ADD, None),
            (self.URL_NOTES_EDIT, (self.note.slug,)),
            (self.URL_NOTES_DELETE, (self.note.slug,)),
            (self.URL_NOTES_DETAIL, (self.note.slug,)),
        )
