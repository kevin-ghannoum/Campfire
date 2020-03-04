from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_post),
    path('feed/', views.feed),
    path('post/', views.post),
]