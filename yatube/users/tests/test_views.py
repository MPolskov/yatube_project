from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django import forms

from users.forms import CreationForm

from users.tests.constants import (
    SIGNUP_URL_NAME
)

User = get_user_model()


class UsersViewsTests(TestCase):

    def test_view_form_context(self):
        """Шаблон создания нового пользователя
         сформирован с правильной формой.
         """
        data = [
            (SIGNUP_URL_NAME, {}),
        ]
        for url_name, kwargs in data:
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                form = response.context.get('form')
                self.assertIsInstance(form, CreationForm)
                form_fields = {
                    'first_name': forms.fields.CharField,
                    'last_name': forms.fields.CharField,
                    'username': forms.fields.CharField,
                    'email': forms.fields.EmailField
                }
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = (form.fields.get(value))
                        self.assertIsNotNone(form_field)
                        self.assertIsInstance(form_field, expected)
