from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post, Group, User, Comment
from .forms import PostForm, CommentForm
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    """Возращает 10 постов отсортированных по дате"""
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


class JustStaticPage(TemplateView):
    template_name = 'just_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Очень простая страница'
        context['text'] = 'На создание этой страницы уменя \
							ушло меньше 10 минут! Ай да я!'
        return context


class Group_posts(DetailView):
    """Возращает 10 постов указанной темы"""
    template_name = 'posts/group_list.html'
    model = Group

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_post = Post.objects.filter(group_id=int(context['object'].id))
        paginator = Paginator(all_post, 10)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page
        context['group'] = context['object']
        return context


def profile(request, username):
    """Показывается профиль пользователя"""
    userobject = User.objects.get(username=username)
    posts = Post.objects.filter(author=userobject).order_by('-pub_date')
    count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    post_last = Post.objects.filter(author=userobject).latest('id')
    return render(request, 'profile.html', {
        'page': page,
        'count': count,
        'userobject': userobject,
        'post_last': post_last
    })


def post_view(request, username, post_id):
    """Показывается пост"""
    userobject = User.objects.get(username=username)
    postobject = Post.objects.get(id=post_id)
    count = Post.objects.filter(author=userobject).count()
    comments = Comment.objects.filter(post=postobject)
    form = CommentForm()

    return render(request, 'post.html', {
        'userobject': userobject,
        'postobject': postobject,
        'count': count,
        'comments': comments,
        'form': form
    })


def post_create(request):
    """Создаётся новый пост"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            username = request.user
            files = form.cleaned_data['image']
            post = Post()
            post.image = files
            post.text = text
            objectuser = User.objects.filter(username=username)
            post.author = objectuser[0]
            objectgroup = Group.objects.filter(id=group)
            post.group = objectgroup[0]
            post.save()
            return HttpResponseRedirect(
                f'/profile/{username}',
                 RequestContext(request)
            )
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


# фича с группой
def post_edit(request, post_id):
    """Редактируется пост"""

    postobject = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            username = request.user
            files = form.cleaned_data['image']
            post = Post()
            post.id = post_id
            post.text = text
            objectuser = User.objects.filter(username=username)
            post.author = objectuser[0]
            objectgroup = Group.objects.filter(id=group)
            post.group = objectgroup[0]
            post.pub_date = datetime.now()
            post.image = files
            post.save()
            return HttpResponseRedirect(
                f'/profile/{username}',
                RequestContext(request)
            )
    else:
        form = PostForm(initial={'text': postobject.text})

    return render(request, 'posts/post_edit.html', {
        'form': form,
        'post_id': post_id
    })


@login_required
def add_comment(request, post_id):
    """Добавляется коммент к посту"""
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        text = form.cleaned_data['text']
        comment = Comment()
        comment.author = request.user
        comment.post = post
        comment.text = text
        comment.save()
    return redirect('posts:post', post_id=post_id, username=request.user)
