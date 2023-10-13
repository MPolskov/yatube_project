from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

USER_USERNAME = 'TestUser'

AUTHOR_URL_NAME = 'about:author'
TECH_URL_NAME = 'about:tech'

AUTHOR_URL_TEMPLATE = 'about/author.html'
TECH_URL_TEMPLATE = 'about/tech.html'

User = get_user_model()


class AboutTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username=USER_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def tearDown(self):
        cache.clear()

    def test_about_url_exists(self):
        """Проверка доступности страниц приложения about
        любому пользователю.
        """
        about_url = [
            AUTHOR_URL_NAME,
            TECH_URL_NAME,
        ]
        for url_name in about_url:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна '
                    'анонимному пользователю'
                )
                response = self.authorized_client.get(reverse(url_name))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна '
                    'авторизированному пользователю'
                )

    def test_correct_template(self):
        """URL-адрес приложения about использует соответствующий шаблон."""
        url_template_names = {
            AUTHOR_URL_NAME: AUTHOR_URL_TEMPLATE,
            TECH_URL_NAME: TECH_URL_TEMPLATE,
        }
        for url_name, template in url_template_names.items():
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Не получен ожидаемый шаблон для адреса {url_name}'
                    f'Ожидаемый шаблон {template}'
                )
