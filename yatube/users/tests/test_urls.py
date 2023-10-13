from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.tests.constants import (
    USER_USERNAME,
    SIGNUP_URL_NAME,
    LOGIN_URL_NAME,
    LOGOUT_URL_NAME,
    PASSWORD_CHANGE_URL_NAME,
    PASSWORD_CHANGE_COMPLETE_URL_NAME,
    PASSWORD_RESET_FORM_URL_NAME,
    PASSWORD_RESET_DONE_URL_NAME,
    PASSWORD_RESET_CONFIRM_URL_NAME,
    PASSWORD_RESET_COMPLETE_URL_NAME,

    SIGNUP_TEMPLATE,
    LOGIN_TEMPLATE,
    LOGOUT_TEMPLATE,
    PASSWORD_CHANGE_TEMPLATE,
    PASSWORD_CHANGE_COMPLETE_TEMPLATE,
    PASSWORD_RESET_FORM_TEMPLATE,
    PASSWORD_RESET_DONE_TEMPLATE,
    PASSWORD_RESET_CONFIRM_TEMPLATE,
    PASSWORD_RESET_COMPLETE_TEMPLATE
)

User = get_user_model()


class UsersURLTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username=USER_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_url_exists_for_anonymous(self):
        """Проверка доступности страниц приложения users
        для анонимного пользователя.
        """
        users_url = {
            SIGNUP_URL_NAME: {},
            LOGIN_URL_NAME: {},
            PASSWORD_RESET_FORM_URL_NAME: {},
            PASSWORD_RESET_DONE_URL_NAME: {},
            PASSWORD_RESET_CONFIRM_URL_NAME:
            {'uidb64': 'uidb64', 'token': 'token'},
            PASSWORD_RESET_COMPLETE_URL_NAME: {}
        }
        for url_name, kwargs in users_url.items():
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна анонимному пользователю'
                )

    def test_users_url_exists_for_authorized_user_only(self):
        """Проверка доступности страниц приложения users
        для авторизованного пользователя пользователя.
        """
        users_url = [
            PASSWORD_CHANGE_URL_NAME,
            PASSWORD_CHANGE_COMPLETE_URL_NAME,
            LOGOUT_URL_NAME,
        ]
        for url_name in users_url:
            with self.subTest(url_name=url_name):
                response = self.authorized_client.get(reverse(url_name))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK.value,
                    f'Страница {url_name} не досупна '
                    'авторизированному пользователю'
                )

    def test_urls_uses_correct_template(self):
        """URL-адрес приложения users использует соответствующий шаблон."""
        url_template_names = {
            SIGNUP_URL_NAME: (
                {}, SIGNUP_TEMPLATE
            ),
            LOGIN_URL_NAME: (
                {}, LOGIN_TEMPLATE
            ),
            PASSWORD_CHANGE_URL_NAME: (
                {}, PASSWORD_CHANGE_TEMPLATE
            ),
            PASSWORD_CHANGE_COMPLETE_URL_NAME: (
                {}, PASSWORD_CHANGE_COMPLETE_TEMPLATE
            ),
            PASSWORD_RESET_FORM_URL_NAME: (
                {}, PASSWORD_RESET_FORM_TEMPLATE
            ),
            PASSWORD_RESET_DONE_URL_NAME: (
                {}, PASSWORD_RESET_DONE_TEMPLATE
            ),
            PASSWORD_RESET_CONFIRM_URL_NAME: (
                {'uidb64': 'uidb64', 'token': 'token'},
                PASSWORD_RESET_CONFIRM_TEMPLATE
            ),
            PASSWORD_RESET_COMPLETE_URL_NAME: (
                {}, PASSWORD_RESET_COMPLETE_TEMPLATE
            ),
            LOGOUT_URL_NAME: (
                {}, LOGOUT_TEMPLATE
            )
        }
        for url_name, params in url_template_names.items():
            kwargs, template = params
            with self.subTest(url_name=url_name):
                response = self.authorized_client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Не получен ожидаемый шаблон для адреса {url_name}'
                    f'Ожидаемый шаблон {template}'
                )
