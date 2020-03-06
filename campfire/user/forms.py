from datetime import datetime
from django import forms
from campfire.user.models import Post, Comment

class ModelFormForPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        exclude = ['user_name']


class ModelFormForComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        exclude = ['user_name','post_key']
