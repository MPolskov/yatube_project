from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма создания поста"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = 'Группа не выбрана'

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        widgets = {
            'text': forms.Textarea(),
        }


class CommentForm(forms.ModelForm):
    """Форма создания комментария"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(),
        }
