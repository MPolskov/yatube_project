from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.tests.constants import (
    SIGNUP_URL_NAME
)

User = get_user_model()


class PostCreateFormTests(TestCase):

    def test_create_user(self):
        """Валидная форма создает пользователя."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'username': 'new_user',
            'email': 'example@mail.com',
            'password1': 'agjkshrgajijodgs12',
            'password2': 'agjkshrgajijodgs12'
        }
        response = self.client.post(
            reverse(SIGNUP_URL_NAME),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:index')
        )
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name='Новый',
                last_name='Пользователь',
                username='new_user',
                email='example@mail.com'
            ).exists()
        )
