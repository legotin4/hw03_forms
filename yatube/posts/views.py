from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post, Group, User, Comment
from .forms import PostForm, CommentForm
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


def index(request):
    """Возращает 10 постов отсортированных по дате"""
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page_obj': page_obj})


class JustStaticPage(TemplateView):
    template_name = 'just_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Очень простая страница'
        context['text'] = 'На создание этой страницы уменя \
                            ушло меньше 10 минут! Ай да я!'
        return context


def group_posts(request, slug):
    """Возращает 10 постов указанной темы"""
    group = get_object_or_404(Group, slug=slug)
    all_post = Post.objects.filter(group=group).order_by("-pub_date").all()
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
    posts = Post.objects.filter(author=author).order_by('-pub_date')
    #posts = author.posts.all()
    count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    '''post_last = Post.objects.filter(author=author).latest('id')'''
    return render(request, 'posts/profile.html', {
        'page_obj': page_obj,
        'count': count,
        'author': author
    })


def post_detail(request, post_id):
    """Показывает пост"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    form = CommentForm()
    print(post.author.username)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def post_create(request):
    """Создаёт новый пост"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(
                'posts:profile',
                username=request.user.username
            )
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


# фича с группой
@login_required
def post_edit(request, post_id):
    """Редактирует пост"""
    postobject = get_object_or_404(
        Post,
        id=post_id,
        author__username=request.user.username
    )
    if request.user.username != postobject.author.username:
        return redirect(
            'post',
            username=request.user.username,
            post_id=post_id
        )
    if request.method == 'POST':
        form = PostForm(request.POST, instance=postobject)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                f'/posts/{post_id}',
                RequestContext(request)
            )
    else:
        form = PostForm(initial={'text': postobject.text})
    return render(request, 'posts/post_edit.html', {
        'form': form,
        'post_id': post_id,
        'is_edit': True
    })


@login_required
def add_comment(request, post_id):
    """Добавляет коммент к посту"""
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
