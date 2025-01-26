from django.contrib.auth import login, get_user_model, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Follow
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserEditForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = get_user_model().objects.filter(email=email).first()
        if user and user.check_password(password):
            login(request, user)
            return redirect('/')
        return render(request, 'user/login.html', {'error_message': 'Invalid login or password.'})
    
    return render(request, 'user/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('login')
    return render(request, 'user/logout.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

def settings(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = CustomUserEditForm(request.POST, request)
        form.set_request(request)
        if form.is_valid():
            form.save()
            return render(request, 'core/settings.html', {'success': "Successfully updated!"})
        return render(request, 'core/settings.html', {'error_message': form.errors})
    
    return render(request, 'core/settings.html')

def profile(request, userhandle):
    user_profile = get_object_or_404(CustomUser, username=userhandle)
    posts_self = user_profile.posts.all()

    is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()
    return render(request, 'core/profile.html', {
        'user': user_profile,
        'posts_self': posts_self,
        'is_following': is_following,
    })

def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself")
        return redirect('profile', userhandle=user_to_follow.username)
    
    existing_follow = Follow.objects.filter(follower=request.user, followed=user_to_follow).first()
    if existing_follow:
        existing_follow.delete()
        messages.success(request, f"You have unfollowed {user_to_follow.display_name}.")
    else:
        Follow.objects.create(follower=request.user, followed=user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.display_name}.")
    
    return redirect('profile', userhandle=user_to_follow.username)
