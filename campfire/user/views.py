from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ModelFormForPost, ModelFormForComment, ModelFormForFollow
from campfire.user.models import Post, Comment, Follow, Like
from campfire.settings import MEDIA_URL
from django.shortcuts import get_object_or_404, redirect
import sqlite3

def logout_view(request):
    if request.method == "POST":
        logout(request)

        return redirect('login')

@csrf_exempt
@login_required(login_url='/login')
def upload_post(request):
    if request.method == 'POST':
        form = ModelFormForPost(request.POST, request.FILES, instance = Post(username=request.user.username))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/feed')
    else:
        form = ModelFormForPost()
    return render(request, 'upload.html', {'form': form})


@login_required(login_url='/login')
def feed(request):
    posts = []
    follows = Follow.objects.filter(username=request.user.username)
    for f in follows:
        posts += Post.objects.filter(username=f.following)
    return render(request, 'feed.html', {'MEDIA_URL': MEDIA_URL, 'posts': posts})

@login_required(login_url='/login')
def fire(request):
    likes = Like.objects.filter(username=request.user.username)
    posts = []
    for l in likes:
        posts += Post.objects.filter(id =l.post_key)
    return render(request, 'fire.html', {'MEDIA_URL': MEDIA_URL, 'posts': posts})

@csrf_exempt
@login_required(login_url='/login')
def post(request):
    post = Post.objects.get(id=request.GET['post_id'])
    print(Like.objects.filter(post_key=request.GET['post_id'], username=request.user.username))
    if Like.objects.filter(post_key=request.GET['post_id'], username=request.user.username).exists():
        is_Liked = True
    else:
        is_Liked = False
    if request.POST.get(' '):
        is_Liked = False
        if Like.objects.filter(post_key=request.GET['post_id'], username=request.user.username).exists():
            Like.objects.filter(post_key=request.GET['post_id'], username=request.user.username).delete()
            is_Liked = False
        else:
            Like.objects.create(username=request.user.username, post_key=request.GET['post_id'])
            is_Liked = True

    comments = Comment.objects.filter(post_key=request.GET['post_id'])
    form = ModelFormForComment(request.POST, instance = Comment(username=request.user.username, post_key=request.GET['post_id']))
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/post/?post_id=' + request.GET['post_id'])
    return render(request, 'post.html', {'MEDIA_URL': MEDIA_URL, 'post': post, 'is_Liked': is_Liked, 'comments': comments, 'form': form})


@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/feed')
        return render(request, 'register.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/feed')
        return render(request, 'login.html', {'form': form})


@csrf_exempt
@login_required(login_url='/login')
def profile(request):
    posts = Post.objects.filter(username=request.user.username)
    form = ModelFormForFollow(request.POST, instance = Follow(username=request.user.username))
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'profile.html', {'MEDIA_URL': MEDIA_URL, 'posts': posts, 'form': form})

