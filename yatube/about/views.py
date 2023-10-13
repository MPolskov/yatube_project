from django.views.generic.base import TemplateView

USE_TECH = [
    'Python',
    'Django',
    'SQLite',
    'VS Code',
    'Git/GitHub',
]


class AboutAuthorView(TemplateView):
    """Класс страницы Об авторе"""
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе проекта'

        return context


class AboutTechView(TemplateView):
    """Класс страницы используемых техналогий"""
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['techs'] = USE_TECH

        return context
