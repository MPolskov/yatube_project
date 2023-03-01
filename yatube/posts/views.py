from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Group

NUM_POSTS_ON_PAGE = 10


def index(request):
    template = 'posts/index.html'
    # posts = Post.objects.all()[:NUM_POSTS_ON_PAGE]
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, NUM_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,  # 'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:NUM_POSTS_ON_PAGE]
    title = group.__str__()
    context = {
        'title': title,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
