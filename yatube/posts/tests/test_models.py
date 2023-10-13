from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post
from posts.tests.constants import (
    USER_USERNAME,
    GROUP_TITLE,
    GROUP_SLUG,
    GROUP_DESCRIPTION,
    POST_TEXT,
)

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_USERNAME)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
        )

    def test_verbose_name(self):
        """Проверяем параметр verbose_name у полей подели Post"""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, exp_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    exp_value,
                    f'Значение verbose_name поля {field} '
                    'не соответствует ожидаемому значению '
                    f'"{exp_value}"'
                )

    def test_help_text(self):
        """Проверяем параметр help_text у полей модели Post"""
        post = PostModelTest.post
        field_help_text = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, exp_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text,
                    exp_value,
                    f'Значение help_text поля {field} '
                    'не соответствует ожидаемому значению '
                    f'"{exp_value}"'
                )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group

        exp_post_str = post.text[:15]
        exp_group_str = group.title

        self.assertEqual(exp_group_str, str(group))
        self.assertEqual(exp_post_str, str(post))
