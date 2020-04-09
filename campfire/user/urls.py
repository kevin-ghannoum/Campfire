from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_post, name="upload"),
    path('feed/', views.feed, name="feed"),
    path('post/', views.post),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.login_view, name="home"),
    path('profile/', views.profile, name="profile"),
    path('fire/', views.fire, name="fire"),  
]