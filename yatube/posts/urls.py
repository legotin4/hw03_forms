from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [

    path('', views.index, name='index'),
    path('justpage/', views.JustStaticPage.as_view()),
    path('group/<str:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<str:username>/post/<int:post_id>/', views.post_view, name='post'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/comment', views.add_comment, name='add_comment')

]
