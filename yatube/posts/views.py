from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm
from .utils import get_paginator
from yatube.settings import NUM_POSTS_ON_PAGE


@cache_page(20, key_prefix='index_page')
def index(request):
    """Функция представления главной страницы"""
    template = 'posts/index.html'
    posts_list = Post.objects.select_related('author', 'group').all()
    page_obj = get_paginator(request, posts_list, NUM_POSTS_ON_PAGE)
    context = {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Функция представления страницы с постами выбранной группы"""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.select_related('author').all()
    page_obj = get_paginator(request, posts_list, NUM_POSTS_ON_PAGE)
    title = group.__str__()
    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Функция представления страницы профайла пользователя"""
    following = False
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.select_related('group').all()
    page_obj = get_paginator(request, posts_list, NUM_POSTS_ON_PAGE)
    num_posts = len(posts_list)
    title = author.__str__()
    if (request.user.is_authenticated
        and (Follow.objects
                   .filter(user=request.user, author=author)
                   .exists())):
        following = True
    context = {
        'title': title,
        'author': author,
        'page_obj': page_obj,
        'num_posts': num_posts,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Функция представления страницы отдельного поста"""
    template = 'posts/post_detail.html'
    post = get_object_or_404(
        Post.objects.select_related('author', 'group').all(),
        pk=post_id
    )
    num_posts = post.author.posts.count()
    comments = post.comments.select_related('author').all()
    title = 'Пост ' + str(post.text[:30])
    comment_form = CommentForm()
    context = {
        'title': title,
        'num_posts': num_posts,
        'post': post,
        'form': comment_form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Функция представления страницы создания поста"""
    if request.method == 'POST':
        form = PostForm(request.POST or None,
                        files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            username = request.user
            post.author = username
            form.save()
            return redirect('posts:profile', username)
    else:
        form = PostForm()

    template = 'posts/create_post.html'
    context = {
        'title': 'Добавить запись',
        'form': form
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """Функция представления страницы изменения поста"""
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(
                request.POST or None,
                files=request.FILES or None,
                instance=post
            )
            if form.is_valid():
                post.text = form.cleaned_data['text']
                post.group = form.cleaned_data['group']
                post.image = form.cleaned_data['image']
                form.save()
                return redirect('posts:post_detail', post_id)

        form = PostForm(instance=post)
        template = 'posts/create_post.html'
        context = {
            'title': 'Редактировать запись',
            'form': form,
            'is_edit': is_edit,
            'post': post
        }

        return render(request, template, context)
    else:
        return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Функция представления страницы подписок"""
    template = 'posts/follow.html'
    authors = request.user.follower.values('author')
    posts_list = (Post.objects
                      .filter(author__in=authors)
                      .select_related('author', 'group'))
    page_obj = get_paginator(request, posts_list, NUM_POSTS_ON_PAGE)
    context = {
        'title': 'Подписки',
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Подписаться на автора"""
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect(
            'posts:profile',
            author.username
        )
    if not (
        Follow.objects
        .filter(user=request.user, author=author)
        .exists()
    ):
        Follow.objects.create(
            user=request.user,
            author=author
        )
        return redirect(
            'posts:profile',
            author.username
        )
    return redirect(
        'posts:profile',
        author.username
    )


@login_required
def profile_unfollow(request, username):
    """Отписаться от автора"""
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect(
            'posts:profile',
            author.username
        )
    if (Follow.objects
              .filter(user=request.user, author=author)
              .exists()):
        Follow.objects.filter(
            user=request.user,
            author=author
        ).delete()
        return redirect(
            'posts:profile',
            author.username
        )
