from django.db import models

class Post(models.Model):
    username = models.CharField(max_length=31)
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    username = models.CharField(max_length=31)
    comment = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now=True)
    post_key = models.IntegerField()

class Follow(models.Model):
    username = models.CharField(max_length=31)
    following = models.CharField(max_length=31)

class Like(models.Model):
    username = models.CharField(max_length=31)
    liked_time = models.DateTimeField(auto_now=True)
    post_key = models.IntegerField()

