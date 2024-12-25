from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestRouters(TestCase):

    def test_home_page(self):
        """Главная страница доступна анонимному пользователю."""
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
