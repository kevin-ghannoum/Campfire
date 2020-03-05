from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ModelFormForPost, ModelFormForComment
from campfire.user.models import Post, Comment
from campfire.settings import MEDIA_URL
from django.shortcuts import get_object_or_404, redirect

def logout_view(request):
    if request.method == "POST":
        logout(request)

        return redirect('login')

@csrf_exempt
@login_required(login_url='/login')
def upload_post(request):
    if request.method == 'POST':
        form = ModelFormForPost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/feed')
    else:
        form = ModelFormForPost()
    return render(request, 'upload.html', {'form': form})


@login_required(login_url='/login')
def feed(request):
    posts = Post.objects.all()
    return render(request, 'feed.html', {'MEDIA_URL': MEDIA_URL, 'posts': posts})


@csrf_exempt
@login_required(login_url='/login')
def post(request):
    post = Post.objects.get(id=request.GET['post_id'])
    comments = Comment.objects.filter(post_key=request.GET['post_id'])
    form = ModelFormForComment(request.POST, instance = Comment(post_key = request.GET['post_id']))
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/post/?post_id=' + request.GET['post_id'])
    return render(request, 'post.html', {'MEDIA_URL': MEDIA_URL, 'post': post, 'comments': comments, 'form': form})


@csrf_exempt
def register(request):
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
