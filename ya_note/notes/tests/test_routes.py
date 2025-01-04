from http import HTTPStatus

from django.urls import reverse

from . import fixtures


class TestRouters(fixtures.Fixtures):
    def test_availability_pages(self):
        """Страницы, доступные анонимному пользователю."""
        for name, args in self.PUBLIC_URLS:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_create_availability(self):
        """Аутентифицированному пользователю доступны notes/, done/ и add/."""
        user = self.author
        status = HTTPStatus.OK
        self.client.force_login(user)
        for name in self.FOR_AUTH_URLS:
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
            # не получилось, попробовал как смог, в гугле ответ тоже не нашел
            # уперся в то, что не могу получить экземпляр нужного юзера
            for name in self.PRIVATE_AUTH_URLS:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Редирект касаемый заметок, для анонимного пользователя."""
        for name, args in self.get_redirect_urls_data():
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{self.URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
