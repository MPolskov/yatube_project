# Для импорта в тесты:
# from .constants import (
#     AUTHOR_USERNAME,
#     USER_USERNAME,
#     GROUP_TITLE,
#     GROUP_SLUG,
#     GROUP_DESCRIPTION,
#     POST_TEXT,
#     INDEX_URL_NAME,
#     GROUP_LIST_URL_NAME,
#     PROFILE_URL_NAME,
#     POST_DETAIL_URL_NAME,
#     POST_CREATE_URL_NAME,
#     POST_EDIT_URL_NAME,
#     INDEX_TEMPLATE,
#     GROUP_LIST_TEMPLATE,
#     PROFILE_TEMPLATE,
#     POST_DETAIL_TEMPLATE,
#     POST_CREATE_TEMPLATE,
#     POST_EDIT_TEMPLATE
# )
AUTHOR_USERNAME = 'TestAuthor'
USER_USERNAME = 'TestUser'
GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Тестовое описание'
POST_TEXT = 'Тестовый текст'

INDEX_URL_NAME = 'posts:index'
GROUP_LIST_URL_NAME = 'posts:group_list'
PROFILE_URL_NAME = 'posts:profile'
POST_DETAIL_URL_NAME = 'posts:post_detail'
POST_CREATE_URL_NAME = 'posts:post_create'
POST_EDIT_URL_NAME = 'posts:post_edit'
POST_COMMENT_URL_NAME = 'posts:add_comment'
POST_FOLLOW_INDEX_URL_NAME = 'posts:follow_index'
PROFILE_FOLLOW_URL_NAME = 'posts:profile_follow'
PROFILE_UNFOLLOW_URL_NAME = 'posts:profile_unfollow'
UNEXISTING_URL = '/unexisting_url/'

INDEX_TEMPLATE = 'posts/index.html'
GROUP_LIST_TEMPLATE = 'posts/group_list.html'
PROFILE_TEMPLATE = 'posts/profile.html'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'
POST_CREATE_TEMPLATE = 'posts/create_post.html'
POST_EDIT_TEMPLATE = 'posts/create_post.html'
