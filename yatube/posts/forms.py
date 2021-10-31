from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Комментарий')
