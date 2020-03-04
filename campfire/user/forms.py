from datetime import datetime
from django import forms
from campfire.user.models import Post, Comment

class ModelFormForPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user_name', 'image', 'caption']


class ModelFormForComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'comment']
        exclude = ['post_key']
