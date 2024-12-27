from http import HTTPStatus

from notes.forms import WARNING, NoteForm
from notes.models import Note
from pytils.translit import slugify

from . import fixtures


class TestLogic(fixtures.Fixtures):

    def test_anonim_cant_create_note(self):
        """Аноним не может создавать заметки."""
        self.client.post(self.url_add, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_logged_user_can_create_note(self):
        """Залогиненый юзер может создавать заметки."""
        self.author_client.post(self.url_add, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 2)

    def test_no_possible_two_same_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        self.form_data.update({'slug': self.SLUG_TITLE})
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.SLUG_TITLE + WARNING
        )
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_automatic_slug_generation(self):
        """Slug формируется автоматически, если не был заполнен."""
        form = NoteForm(data=self.form_data)
        form.full_clean()
        self.assertEqual(
            form.cleaned_data['slug'],
            slugify(self.form_data[self.SLUG_TITLE])
        )

    def test_author_can_edit_his_notes(self):
        """Автор может редактировать свои заметки."""
        response = self.author_client.post(
            self.url_edit,
            data=self.form_data
        )
        self.assertRedirects(response, self.url_success)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_author_can_delete_his_notes(self):
        """Автор может удалять свои заметки."""
        response = self.author_client.post(self.url_delete)
        self.assertRedirects(response, self.url_success)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_user_cant_edit_another_users_notes(self):
        """Пользователь не может редактировать чужие заметки."""
        response = self.reader_client.post(
            self.url_edit,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)

    def test_user_cant_delele_another_users_notes(self):
        """Пользователь не может удалять чужие заметки."""
        response = self.reader_client.post(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
