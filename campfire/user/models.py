from django.db import models

class Post(models.Model):
    user_name = models.CharField(max_length=31)
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now=True)
