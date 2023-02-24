from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    template = 'posts/index.html'
    context = {
        'title': 'Yatube',
        'text': 'Это главная страница проекта Yatube'
    }
    return render(request, template, context)


def group_list(request):
    template = 'posts/group_list.html'
    return render(request, template)


def group_posts(request, slug):

    context = {
        'title': 'Groups',
        'text': 'Здесь будет информация о группах проекта Yatube'
    }
    return HttpResponse(f'Посты сгруппированные по {slug}')
