from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Group

def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'title': 'Yatube',
        'text': 'Это главная страница проекта Yatube',
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'title': 'Группы Yatube',
        'group': group,
        'posts': posts,
        'text': 'Здесь будет информация о группах проекта Yatube'
    }
    return render(request, template, context)

