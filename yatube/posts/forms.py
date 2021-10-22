from django import forms
from .models import Group


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Текст поста*')
    group = forms.ChoiceField(label='Группа', choices=Group.objects.all(
    ).values_list('id', 'slug'), required=False)
    image = forms.ImageField(label='Изображение')


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Комментарий')
