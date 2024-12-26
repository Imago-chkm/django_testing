from http import HTTPStatus

from django.urls import reverse

from . import fixtures


class TestRouters(fixtures.Fixtures):

    def test_availability_pages(self):
        """Страницы, доступные анонимному пользователю."""
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_create_availability(self):
        """Аутентифицированному пользователю доступны notes/, done/ и add/."""
        user = self.author
        status = HTTPStatus.OK
        self.client.force_login(user)
        for name in (
            self.URL_NOTES_LIST,
            self.URL_NOTES_ADD,
            self.URL_NOTES_SUCCESS
        ):
            with self.subTest(user=user, name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_author_notes_availability(self):
        """Доступ автору к заметкам, их удалению/редактированию."""
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (
                self.URL_NOTES_EDIT,
                self.URL_NOTES_DELETE,
                self.URL_NOTES_DETAIL
            ):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Редирект касаемый заметок, для анонимного пользователя."""
        login_url = reverse('users:login')
        urls = (
            (self.URL_NOTES_LIST, None),
            (self.URL_NOTES_SUCCESS, None),
            (self.URL_NOTES_ADD, None),
            (self.URL_NOTES_EDIT, (self.note.slug,)),
            (self.URL_NOTES_DELETE, (self.note.slug,)),
            (self.URL_NOTES_DETAIL, (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
