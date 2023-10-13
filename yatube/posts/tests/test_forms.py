import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from posts.forms import PostForm
from posts.models import Post, Group, Comment
from posts.tests.constants import (
    AUTHOR_USERNAME,
    GROUP_TITLE,
    GROUP_SLUG,
    GROUP_DESCRIPTION,
    POST_TEXT,
    POST_CREATE_URL_NAME,
    PROFILE_URL_NAME,
    POST_EDIT_URL_NAME,
    POST_DETAIL_URL_NAME,
    POST_COMMENT_URL_NAME
)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR_USERNAME)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION
        )
        cls.form = PostForm()
        Post.objects.create(
            text=POST_TEXT,
            author=PostCreateFormTests.author,
            group=PostCreateFormTests.group
        )

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def tearDown(self):
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'text': POST_TEXT + 'new',
            'group': PostCreateFormTests.group.id,
            'image': uploaded,
        }
        response = self.author_client.post(
            reverse(POST_CREATE_URL_NAME),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(PROFILE_URL_NAME,
                    kwargs={'username': self.author.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=POST_TEXT + 'new',
                group=PostCreateFormTests.group,
                image='posts/small.gif'
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        posts_count = Post.objects.count()
        edit_data = {
            'text': 'Отредактированный текст',
            'group': PostCreateFormTests.group.id
        }
        response = self.author_client.post(
            reverse(POST_EDIT_URL_NAME,
                    kwargs={'post_id': Post.objects.latest('pk').id}),
            data=edit_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(POST_DETAIL_URL_NAME,
                    kwargs={'post_id': response.context.get('post').id})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный текст',
                group=PostCreateFormTests.group
            ).exists()
        )
        self.assertFalse(
            Post.objects.filter(
                text=POST_TEXT,
                group=PostCreateFormTests.group
            ).exists()
        )

    def test_create_comment(self):
        """Проверка создания комментария"""
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Комментарий'
        }
        response = self.author_client.post(
            reverse(POST_COMMENT_URL_NAME,
                    kwargs={'post_id': Post.objects.latest('pk').id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(POST_DETAIL_URL_NAME,
                    kwargs={'post_id': response.context.get('post').id})
        )
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text='Комментарий',
                post=response.context.get('post').id
            ).exists()
        )
