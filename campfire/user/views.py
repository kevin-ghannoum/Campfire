from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ModelFormForPost
from campfire.user.models import Post

@csrf_exempt
def upload_post(request):
    if request.method == 'POST':
        form = ModelFormForPost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/upload')
    else:
        form = ModelFormForPost()
    return render(request, 'upload.html', {'form': form})