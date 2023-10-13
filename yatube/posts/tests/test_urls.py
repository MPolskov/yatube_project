from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

from posts.models import Post, Group
from posts.tests.constants import (
    AUTHOR_USERNAME,
    USER_USERNAME,
    GROUP_TITLE,
    GROUP_SLUG,
    GROUP_DESCRIPTION,
    POST_TEXT,
    INDEX_URL_NAME,
    GROUP_LIST_URL_NAME,
    PROFILE_URL_NAME,
    POST_DETAIL_URL_NAME,
    POST_CREATE_URL_NAME,
    POST_EDIT_URL_NAME,
    POST_COMMENT_URL_NAME,
    POST_FOLLOW_INDEX_URL_NAME,
    INDEX_TEMPLATE,
    GROUP_LIST_TEMPLATE,
    PROFILE_TEMPLATE,
    POST_DETAIL_TEMPLATE,
    POST_CREATE_TEMPLATE,
    POST_EDIT_TEMPLATE,
    UNEXISTING_URL
)
from users.tests.constants import (
    LOGIN_URL_NAME
)

User = get_user_model()


class StaticURLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_USERNAME)
        cls.author = User.objects.create_user(username=AUTHOR_USERNAME)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        Post.objects.create(
            text=POST_TEXT,
            author=cls.author,
            group=cls.group
        )

    def setUp(self):
        self.authorized_user = Client()
        self.authorized_author = Client()
        self.authorized_user.force_login(PostURLTests.user)
        self.authorized_author.force_login(PostURLTests.author)
        self.post = Post.objects.latest('pk')

    def tearDown(self):
        cache.clear()

    def test_url_404(self):
        """Проверка вызова несуществующей страницы"""
        response = self.client.get(UNEXISTING_URL)
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
            'Анонимный пользователь открыл несуществующую страницу! '
            'Высокий риск наступления события класса "Zero Keter"'
        )
        response = self.authorized_user.get(UNEXISTING_URL)
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
            'Авторизованный пользователь открыл несуществующую страницу! '
            'Высокий риск наступления события класса "Zero Keter"'
        )

    def test_url_exists(self):
        """Проверка url общих страниц любому пользователю."""
        common_url = [
            (INDEX_URL_NAME, {}),
            (GROUP_LIST_URL_NAME, {'slug': PostURLTests.group.slug}),
            (PROFILE_URL_NAME, {'username': PostURLTests.author}),
            (POST_DETAIL_URL_NAME, {'post_id': self.post.id}),
        ]
        for url_name, kwargs in common_url:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна анонимному пользователю'
                )
                response = self.authorized_user.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна '
                    'авторизированному пользователю'
                )

    def test_url_exists_for_authorized_user_only(self):
        """Проверка url требующих авторизации."""
        auth_user_url = [
            (POST_CREATE_URL_NAME, {}),
            (POST_FOLLOW_INDEX_URL_NAME, {})
        ]
        for url_name, kwargs in auth_user_url:
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FOUND,
                    'Анонимный пользователь '
                    f'не перенаправлен со страницы {url_name}'
                )
                response = self.authorized_user.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна '
                    'авторизированному пользователю'
                )

    def test_url_exists_for_author_only(self):
        """Проверка url доступных только автора поста."""
        author_url = [
            (POST_EDIT_URL_NAME, {'post_id': self.post.id}),
        ]
        for url_name, kwargs in author_url:
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FOUND,
                    'Неавторизованный пользователь '
                    f'не перенаправлен со страницы {url_name}'
                )
                response = self.authorized_user.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FOUND,
                    'Неавтор поста'
                    f'не перенаправлен со страницы {url_name}'
                )
                response = self.authorized_author.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {url_name} не досупна автору поста'
                )

    def test_url_redirect_anonymous(self):
        """
        Проверка перенаправления анонимного пользователя
        если страница ему не доступна.
        """
        redirect_url = {
            POST_CREATE_URL_NAME:
            ({}, '?next=/create/'),
            POST_EDIT_URL_NAME:
            ({'post_id': self.post.id},
             f'?next=/posts/{self.post.id}/edit/'),
            POST_COMMENT_URL_NAME:
            ({'post_id': self.post.id},
             f'?next=/posts/{self.post.id}/comment/')
        }
        for url_name, params in redirect_url.items():
            kwargs, next_page = params
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(url_name, kwargs=kwargs),
                    follow=True
                )
                redirect = reverse(LOGIN_URL_NAME) + next_page
                self.assertRedirects(
                    response,
                    redirect,
                    msg_prefix='Ошибка перенаправления '
                    f'анонимного пользователя со страницы {url_name}'
                )

    def test_url_redirect_not_author(self):
        """
        Проверка перенаправления авторизованного пользователя
        если он пытается редактировать пост другого пользователя.
        """
        response = self.authorized_user.get(
            reverse(POST_EDIT_URL_NAME,
                    kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(POST_DETAIL_URL_NAME, kwargs={'post_id': self.post.id}),
            msg_prefix='Ошибка перенаправления не автора поста '
            'на страницу поста при попытке его редактирования'
        )

    def test_urls_uses_correct_template(self):
        """URL-адрес приложения posts использует соответствующий шаблон."""
        url_template_names = {
            INDEX_URL_NAME: (
                INDEX_TEMPLATE, {}
            ),
            GROUP_LIST_URL_NAME: (
                GROUP_LIST_TEMPLATE, {'slug': self.group.slug}
            ),
            PROFILE_URL_NAME: (
                PROFILE_TEMPLATE, {'username': self.user}
            ),
            POST_DETAIL_URL_NAME: (
                POST_DETAIL_TEMPLATE, {'post_id': self.post.id}
            ),
            POST_CREATE_URL_NAME: (
                POST_CREATE_TEMPLATE, {}
            ),
            POST_EDIT_URL_NAME: (
                POST_EDIT_TEMPLATE, {'post_id': self.post.id}
            )
        }
        for url_name, params in url_template_names.items():
            with self.subTest(url_name=url_name):
                template, kwargs = params
                response = self.authorized_author.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Не получен ожидаемый шаблон для адреса {url_name}'
                    f'Ожидаемый шаблон {template}'
                )
