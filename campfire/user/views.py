from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ModelFormForPost, ModelFormForComment
from campfire.user.models import Post, Comment
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


@csrf_exempt
def post(request):
    post = Post.objects.get(id=request.GET['post_id'])
    comments = Comment.objects.filter(post_key=request.GET['post_id'])
    form = ModelFormForComment(request.POST, initial={'post_key': request.GET['post_id']})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/feed')
    return render(request, 'post.html', {'MEDIA_URL': MEDIA_URL, 'post': post, 'comments': comments, 'form': form})
