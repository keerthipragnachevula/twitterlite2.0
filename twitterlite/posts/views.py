from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm, PostForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been shared!")
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


    
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden("You can only delete your own posts.")

    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('home')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts})