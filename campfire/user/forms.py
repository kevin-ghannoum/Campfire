from datetime import datetime
from django import forms
from campfire.user.models import Post, Comment, Follow

class ModelFormForPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        exclude = ['username']


class ModelFormForComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        exclude = ['username','post_key']

class ModelFormForFollow(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['following']
        exclude = ['username']
