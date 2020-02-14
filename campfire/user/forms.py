from datetime import datetime
from django import forms
from campfire.user.models import Post

class ModelFormForPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user_name', 'image', 'caption']