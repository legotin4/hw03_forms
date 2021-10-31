from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
    #text = forms.CharField(widget=forms.Textarea, label='Текст поста*')
    #group = forms.ChoiceField(label='Группа', choices=Group.objects.all(
    #).values_list('id', 'slug'), required=False)
    


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Комментарий')
