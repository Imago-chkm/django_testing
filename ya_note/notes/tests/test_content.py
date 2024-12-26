from django.urls import reverse

from . import fixtures


class TestContent(fixtures.Fixtures):

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
