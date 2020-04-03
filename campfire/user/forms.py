from datetime import datetime
from django import forms
from campfire.user.models import Post, Comment, Follow

class ModelFormForPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        exclude = ['username']


class ModelFormForComment(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Write a comment...'
        }
    ))

    class Meta:
        model = Comment
        fields = ['comment']
        exclude = ['username','post_key']

class ModelFormForFollow(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['following']
        exclude = ['username']
