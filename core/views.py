from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from post.models import Post, Like, Save
from user.models import Follow
from django.db.models import Count

def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        posts = Post.objects.all().order_by('-created_at')
        posts_self = Post.objects.filter(user=request.user).order_by('-created_at')

        following_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
        posts_followed = Post.objects.filter(user__id__in=following_users).order_by('-created_at')

        liked_posts = []
        for liked_post in Like.objects.all():
            if request.user == liked_post.user:
                liked_posts.append(liked_post.post)

        saved_posts = []
        for saved_post in Save.objects.all():
            if request.user == saved_post.user:
                saved_posts.append(saved_post.post)

        posts_trending = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')

        return render(request, 'core/index.html', {
            'posts': posts,
            'posts_self': posts_self,
            'liked_posts': liked_posts,
            'saved_posts': saved_posts,
            'posts_followed': posts_followed,
            'posts_trending': posts_trending,
        })

def profile(request, userhandle):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        User = get_user_model()
        user = get_object_or_404(User, username=userhandle)
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
        posts_self = Post.objects.filter(user=user).order_by('-created_at')
        liked_posts = [like.post for like in Like.objects.filter(user=request.user)]

        return render(request, 'core/profile.html', {
            'user': user,
            'posts_self': posts_self,
            'liked_posts': liked_posts,
            'is_following': is_following,
        })


def liked(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    saved_posts = []
    for saved_post in Save.objects.all():
        if request.user == saved_post.user:
            saved_posts.append(saved_post.post)

    liked_posts = []
    for liked_post in Like.objects.all():
        if request.user == liked_post.user:
            liked_posts.append(liked_post.post)

    return render(request, 'core/liked.html', {
        'saved_posts': saved_posts,
        'liked_posts': liked_posts,
    })

def saved(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    saved_posts = []
    for saved_post in Save.objects.all():
        if request.user == saved_post.user:
            saved_posts.append(saved_post.post)

    liked_posts = []
    for liked_post in Like.objects.all():
        if request.user == liked_post.user:
            liked_posts.append(liked_post.post)

    return render(request, 'core/saved.html', {
        'saved_posts': saved_posts,
        'liked_posts': liked_posts,
    })



