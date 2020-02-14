from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ModelFormForPost
from campfire.user.models import Post
from campfire.settings import MEDIA_URL

@csrf_exempt
def upload_post(request):
    if request.method == 'POST':
        form = ModelFormForPost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/feed')
    else:
        form = ModelFormForPost()
    return render(request, 'upload.html', {'form': form})


def feed(request):
    posts = Post.objects.all()
    return render(request, 'feed.html', {'MEDIA_URL': MEDIA_URL, 'posts': posts})


def post(request):
    posts = Post.objects.all()
    return render(request, 'feed.html', {'MEDIA_URL': MEDIA_URL, 'posts': posts})