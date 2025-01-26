from django.shortcuts import render, redirect,  get_object_or_404
from .forms import PostForm
from .models import Post, Like, Save
from user.models import Follow

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'core/components/feed.html', {
        'form': form,
        'posts': posts,
    })

def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post(user=request.user, content=content)
            post.save()
            return redirect('home')
    return redirect('home')

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:
        post.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    save, created = Save.objects.get_or_create(user=request.user, post=post)
    if not created:
        save.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))