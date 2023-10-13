from http import HTTPStatus
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django import forms
from django.core.paginator import Page
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.core.cache import cache

from posts.models import Post, Group, Follow
from posts.forms import PostForm
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
    # POST_COMMENT_URL_NAME,
    POST_FOLLOW_INDEX_URL_NAME,
    PROFILE_FOLLOW_URL_NAME,
    PROFILE_UNFOLLOW_URL_NAME,
    INDEX_TEMPLATE,
    GROUP_LIST_TEMPLATE,
    PROFILE_TEMPLATE,
    POST_DETAIL_TEMPLATE,
    POST_CREATE_TEMPLATE,
    POST_EDIT_TEMPLATE
)

from yatube.settings import NUM_POSTS_ON_PAGE

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

ADD_POSTS = 13  # Количество создаваемых тестовых постов

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR_USERNAME)
        cls.author_2 = User.objects.create_user(username=AUTHOR_USERNAME + '2')
        cls.user = User.objects.create_user(username=USER_USERNAME)
        cls.user_2 = User.objects.create_user(username=USER_USERNAME + '2')
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        Post.objects.bulk_create(
            [
                Post(
                    text=f'{POST_TEXT} {i}',
                    author=cls.author,
                    group=cls.group,
                    image=cls.uploaded
                ) for i in range(ADD_POSTS)
            ]
        )
        Post.objects.bulk_create(
            [
                Post(
                    text=f'{POST_TEXT} {i} без группы',
                    author=cls.author,
                    image=cls.uploaded
                ) for i in range(ADD_POSTS)
            ]
        )
        Post.objects.bulk_create(
            [
                Post(
                    text=f'{POST_TEXT} {i}',
                    author=cls.author_2
                ) for i in range(ADD_POSTS)
            ]
        )

    def setUp(self):
        self.author_client = Client()
        self.user_client = Client()
        self.user_2_client = Client()
        self.author_client.force_login(self.author)
        self.user_client.force_login(self.user)
        self.user_2_client.force_login(self.user_2)
        self.post = Post.objects.latest('pk')
        self.post_author = (Post.objects
                            .filter(author=self.author)
                            .latest('pk'))
        self.post_group = (Post.objects
                           .filter(group=self.group)
                           .latest('pk'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        cache.clear()

    def test_correct_template(self):
        """Views приложения posts используют соответствующий шаблон."""
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
                POST_EDIT_TEMPLATE, {'post_id': self.post_author.id}
            )
        }
        for url_name, params in url_template_names.items():
            with self.subTest(url_name=url_name):
                template, kwargs = params
                response = self.author_client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Не получен ожидаемый шаблон для адреса {url_name}'
                    f'Ожидаемый шаблон {template}'
                )

    def test_view_form_context(self):
        """Проверка формы для шаблонов create и edit."""
        data = [
            (POST_CREATE_URL_NAME, {}),
            (POST_EDIT_URL_NAME, {'post_id': self.post_author.id})
        ]
        for url_name, kwargs in data:
            with self.subTest(url_name=url_name):
                response = self.author_client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                form = response.context.get('form')
                self.assertIsInstance(form, PostForm)
                form_fields = {
                    'text': forms.fields.CharField,
                    'group': forms.fields.ChoiceField,
                }
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = (form.fields.get(value))
                        self.assertIsNotNone(form_field)
                        self.assertIsInstance(form_field, expected)

    def test_pages_show_correct_post_context(self):
        """Проверка контекста."""
        data = {
            INDEX_URL_NAME: (
                {},
                (self.post.text,
                 self.post.group,
                 self.post.image)
            ),
            GROUP_LIST_URL_NAME: (
                {'slug': PostViewTests.group.slug},
                (self.post_group.text,
                 self.post_group.group,
                 self.post_group.image)
            ),
            PROFILE_URL_NAME: (
                {'username': PostViewTests.author},
                (self.post_author.text,
                 self.post_author.group,
                 self.post_author.image)
            ),
        }
        for url_name, params in data.items():
            kwargs, exp_value = params
            with self.subTest(url_name=url_name):
                response = self.author_client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                first_object = response.context.get('page_obj')[0]
                self.assertIsNotNone(first_object)
                self.assertEqual(first_object.text, exp_value[0])
                self.assertEqual(first_object.group, exp_value[1])
                self.assertEqual(first_object.image, exp_value[2])

    def test_image_post_detail_context(self):
        """Проверка наличия изображения в контексте страницы post_detail"""
        data = {
            POST_DETAIL_URL_NAME: (
                {'post_id': self.post.id},
                (self.post.image)
            ),
        }
        for url_name, params in data.items():
            kwargs, exp_value = params
            with self.subTest(url_name=url_name):
                response = self.author_client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                post = response.context.get('post')
                self.assertIsNotNone(post)
                self.assertEqual(post.image, exp_value)

    def test_correct_view_context(self):
        """
        Проверка ожидаемого контекста страниц
         (кроме пагинатора и форм).
        """
        data = {
            INDEX_URL_NAME: (
                {},
                {'title': 'Последние обновления на сайте'}
            ),
            GROUP_LIST_URL_NAME: (
                {'slug': PostViewTests.group.slug},
                {'title': PostViewTests.group.title,
                 'group': PostViewTests.group}
            ),
            PROFILE_URL_NAME: (
                {'username': PostViewTests.author},
                {'title': str(PostViewTests.author),
                 'author': PostViewTests.author}
            ),
            POST_DETAIL_URL_NAME: (
                {'post_id': self.post.id},
                {'title': 'Пост ' + self.post.text[:30],
                 'post': self.post}
            ),
            POST_CREATE_URL_NAME: (
                {},
                {'title': 'Добавить запись'}
            ),
            POST_EDIT_URL_NAME: (
                {'post_id': self.post_author.id},
                {'title': 'Редактировать запись',
                 'is_edit': True,
                 'post': self.post_author}
            )
        }
        for url_name, params in data.items():
            url_kwargs, context_kwargs = params
            with self.subTest(url_name=url_name):
                response = self.author_client.get(
                    reverse(url_name, kwargs=url_kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                for context, value in context_kwargs.items():
                    with self.subTest(context=context):
                        check_val = response.context.get(context)
                        self.assertIsNotNone(check_val)
                        self.assertEqual(check_val, value)

    def test_paginator(self):
        """Проверка контекста первой страницы пагинатора"""
        urls_expected_post_number = {
            INDEX_URL_NAME: (
                {},
                Post.objects.all()[:NUM_POSTS_ON_PAGE]
            ),
            GROUP_LIST_URL_NAME: (
                {'slug': self.group.slug},
                self.group.posts.all()[:NUM_POSTS_ON_PAGE]
            ),
            PROFILE_URL_NAME: (
                {'username': self.author.username},
                self.author.posts.all()[:NUM_POSTS_ON_PAGE]
            ),
        }
        for url_name, params in urls_expected_post_number.items():
            kwargs, queryset = params
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                page_obj = response.context.get('page_obj')
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertQuerysetEqual(
                    page_obj, queryset, transform=lambda x: x
                )

    def _start_post(self, count):
        """Определение начала среза для test_paginator_last_page"""
        if count % NUM_POSTS_ON_PAGE == 0:
            return (count // NUM_POSTS_ON_PAGE - 1) * NUM_POSTS_ON_PAGE
        return (count // NUM_POSTS_ON_PAGE) * NUM_POSTS_ON_PAGE

    def _last_page(self, count):
        """Определение последней страницы test_paginator_last_page"""
        return (count // NUM_POSTS_ON_PAGE) + 1

    def test_paginator_last_page(self):
        """Проверка контекста последней страницы пагинатора"""
        index_count = Post.objects.all().count()
        group_count = self.group.posts.all().count()
        profile_count = self.author.posts.all().count()
        urls_expected_post_number = {
            INDEX_URL_NAME: (
                {},
                Post.objects.all()[self._start_post(index_count):index_count],
                self._last_page(index_count)
            ),
            GROUP_LIST_URL_NAME: (
                {'slug': self.group.slug},
                self.group.posts.all()[self._start_post(group_count):
                                       group_count],
                self._last_page(group_count)
            ),
            PROFILE_URL_NAME: (
                {'username': self.author.username},
                self.author.posts.all()[self._start_post(profile_count):
                                        profile_count],
                self._last_page(profile_count)
            ),
        }
        for url_name, params in urls_expected_post_number.items():
            kwargs, queryset, last_page = params
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(url_name, kwargs=kwargs) + f'?page={last_page}'
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                page_obj = response.context.get('page_obj')
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertQuerysetEqual(
                    page_obj, queryset, transform=lambda x: x
                )

    def test_show_new_post(self):
        """Проверка отображения нового поста на страницах с постами"""
        self.group_2 = Group.objects.create(
            title=GROUP_TITLE + '2',
            slug=GROUP_SLUG + '2',
            description=GROUP_DESCRIPTION + '2',
        )
        Post.objects.create(
            text=f'{POST_TEXT} дополнительный',
            author=PostViewTests.author,
            group=PostViewTests.group
        )
        data = {
            INDEX_URL_NAME: ({}, Post.objects.latest('pk')),
            GROUP_LIST_URL_NAME: (
                {'slug': PostViewTests.group.slug},
                (Post.objects
                 .filter(group=self.group)
                 .latest('pk'))
            ),
            PROFILE_URL_NAME: (
                {'username': PostViewTests.author},
                (Post.objects
                 .filter(author=self.author)
                 .latest('pk'))
            ),
        }
        for url_name, params in data.items():
            kwargs, exp_value = params
            with self.subTest(url_name=url_name):
                response = self.author_client.get(
                    reverse(url_name, kwargs=kwargs)
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                first_object = response.context.get('page_obj')[0]
                self.assertIsNotNone(first_object)
                self.assertIsInstance(first_object, Post)
                self.assertEqual(first_object, exp_value)

        # Проверка, что пост не попал в другую группу
        kwargs = {'slug': self.group_2.slug}
        response = self.author_client.get(
            reverse(GROUP_LIST_URL_NAME, kwargs=kwargs)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        first_object = response.context.get('page_obj')
        self.assertEqual(len(first_object), 0,
                         'Новый пост отображается в другой группе!')

    def test_cache(self):
        """Проверка кэша"""
        Post.objects.create(
            text=f'{POST_TEXT} дополнительный',
            author=PostViewTests.author,
            group=PostViewTests.group
        )
        response = self.author_client.get(reverse(INDEX_URL_NAME))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content_1 = response.content
        Post.objects.filter(
            text=f'{POST_TEXT} дополнительный',
            author=PostViewTests.author,
            group=PostViewTests.group
        ).delete()
        response = self.author_client.get(reverse(INDEX_URL_NAME))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content_2 = response.content
        self.assertEqual(content_1, content_2)

    def test_following(self):
        """Проверка подписки на автора"""
        follow_count_1 = self.user.follower.count()
        follow_count_2 = self.author_2.follower.count()
        response = self.user_client.get(
            reverse(PROFILE_FOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.user_client.get(
            reverse(PROFILE_FOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author_2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self.user.follower.count(), follow_count_1 + 2)
        self.assertEqual(self.author_2.follower.count(), follow_count_2)

    def test_unfollowing(self):
        """Проверка отписки от автора"""
        response = self.user_client.get(
            reverse(PROFILE_FOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.user_client.get(
            reverse(PROFILE_FOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author_2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        follow_count = self.user.follower.count()
        response = self.user_client.get(
            reverse(PROFILE_UNFOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author_2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self.user.follower.count(), follow_count - 1)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user,
                author=self.author
            ).exists()
        )
        self.assertFalse(
            Follow.objects.filter(
                user=self.user,
                author=self.author_2
            ).exists()
        )

    def test_follow_index_content(self):
        """Новая запись пользователя появляется в ленте тех,
         кто на него подписан и не появляется в ленте тех, кто не подписан.
        """
        # Подписываем польз. на авторов
        self.user_client.get(
            reverse(PROFILE_FOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author})
        )
        self.user_2_client.get(
            reverse(PROFILE_FOLLOW_URL_NAME,
                    kwargs={'username': PostViewTests.author_2})
        )
        user_2_queryset = (Post.objects
                               .filter(author=PostViewTests.author_2)
                           [:NUM_POSTS_ON_PAGE])
        # Создаем новый пост у автора 1
        post = Post.objects.create(
            text='Только что созданный пост',
            author=PostViewTests.author
        )
        user_1_queryset = (Post.objects
                               .filter(author=PostViewTests.author)
                           [:NUM_POSTS_ON_PAGE])
        self.assertIn(post, user_1_queryset)
        # Проверяем, что новый пост отобразился у польз.1
        response = self.user_client.get(
            reverse(POST_FOLLOW_INDEX_URL_NAME)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        page_obj = response.context.get('page_obj')
        self.assertIsNotNone(page_obj)
        self.assertIsInstance(page_obj, Page)
        self.assertQuerysetEqual(
            page_obj, user_1_queryset, transform=lambda x: x
        )
        # Проверяем, что новый пост НЕ отобразился у польз.2
        response = self.user_2_client.get(
            reverse(POST_FOLLOW_INDEX_URL_NAME)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        page_obj = response.context.get('page_obj')
        self.assertIsNotNone(page_obj)
        self.assertIsInstance(page_obj, Page)
        self.assertQuerysetEqual(
            page_obj, user_2_queryset, transform=lambda x: x
        )
