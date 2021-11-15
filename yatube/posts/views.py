from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    """Возращает 10 постов отсортированных по дате"""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page_obj': page_obj})


def group_posts(request, slug):
    """Возращает 10 постов указанной темы"""
    group = get_object_or_404(Group, slug=slug)
    all_post = group.group.all()
    '''Post.objects.filter(group=group).all()'''
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'posts/group_list.html',
        {'page_obj': page_obj, 'group': group}
    )


def profile(request, username):
    """Показывает профиль пользователя"""
    author = get_object_or_404(User, username=username)
    posts = author.posts.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    '''post_last = Post.objects.filter(author=author).latest('id')'''
    return render(request, 'posts/profile.html', {
        'page_obj': page_obj,
        'author': author
    })


def post_detail(request, post_id):
    """Показывает пост"""
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {
        'post': post,
    })


@login_required
def post_create(request):
    """Создаёт новый пост"""
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect(
        'posts:profile',
        username=request.user.username
    )


@login_required
def post_edit(request, post_id):
    """Редактирует пост"""
    postobject = get_object_or_404(
        Post,
        id=post_id
    )
    if request.user.username != postobject.author.username:
        return redirect(
            'posts:post_detail',
            post_id=post_id
        )

    form = PostForm(request.POST or None, instance=postobject)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {
            'form': form,
            'post_id': post_id,
            'is_edit': True
        })
    form.save()
    return redirect('posts:post_detail', post_id=post_id)
