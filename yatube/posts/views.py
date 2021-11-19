from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post, Group, User


def paginatorFunc(posts, request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Возращает 10 постов отсортированных по дате"""
    post_list = Post.objects.all()
    page_obj = paginatorFunc(post_list, request)
    return render(request, 'posts/index.html', {'page_obj': page_obj})


def group_posts(request, slug):
    """Возращает 10 постов указанной темы"""
    group = get_object_or_404(Group, slug=slug)
    all_post = group.post.all()
    page_obj = paginatorFunc(all_post, request)

    return render(
        request,
        'posts/group_list.html',
        {'page_obj': page_obj, 'group': group}
    )


def profile(request, username):
    """Показывает профиль пользователя"""
    author = get_object_or_404(User, username=username)
    posts_all = author.posts.all()
    page_obj = paginatorFunc(posts_all, request)
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
    post = get_object_or_404(
        Post,
        id=post_id
    )
    if request.user != post.author:
        return redirect(
            'posts:post_detail',
            post_id=post_id
        )

    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {
            'form': form,
            'post_id': post_id,
            'is_edit': True
        })
    form.save()
    return redirect('posts:post_detail', post_id=post_id)
