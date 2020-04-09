import os, shutil
import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from campfire.user.models import Post, Follow, Comment, Like
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

first_user = {'username': 'Batman', 'password': 'Wayne8'}
second_user = {'username': 'Spiderman', 'password': 'Parker4'}

first_image_path = 'media/images/campfire_logo.png'

# Create your tests here.
class Test(TestCase):
    def login_first_user(self, create=True):
        if create:
            User.objects.create_user(username=first_user['username'], password=first_user['password'])
        self.client.login(username=first_user['username'], password=first_user['password'])
    
    def login_second_user(self, create=True):
        if create:
            User.objects.create_user(username=second_user['username'], password=second_user['password'])
        self.client.login(username=second_user['username'], password=second_user['password'])
    
    def test_create_users(self):
        self.login_first_user()
        self.client.logout()
        self.login_second_user()
        self.client.logout()
    
    def test_access_register_page(self):
        response = self.client.get('/register/')
        page = response.content.decode('utf8') 
        self.assertIn('<h4>Create an account.</h4>', page)

    def test_access_root_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
    
    def test_redirect_root_to_login(self):
        response = self.client.get('/')
        page = response.content.decode('utf8') 
        self.assertIn('<h4>Login Here.</h4>', page)
    
    def test_access_login_page(self):
        response = self.client.get('/login/')
        page = response.content.decode('utf8') 
        self.assertIn('<h4>Login Here.</h4>', page)

    def test_access_feed_page(self):
        self.login_first_user()
        response = self.client.get('/feed/')
        self.assertEquals(response.status_code, 200)
        self.client.logout()
    
    def test_access_profile_page(self):
        self.login_first_user()
        response = self.client.get('/profile/')
        page = response.content.decode('utf8') 
        self.assertIn('<h1>'+first_user['username']+'</h2>', page)
        self.client.logout()
    
    def test_access_logout_page(self):
        self.login_first_user()
        response = self.client.post('/logout/')
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.client.logout()

    def test_access_fire_page(self):
        self.login_first_user()
        response = self.client.get('/fire/')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_access_upload_page(self):
        self.login_first_user()
        response = self.client.get('/upload/')
        page = response.content.decode('utf8') 
        self.assertIn('<h4>Create a post.</h4>', page)
        self.client.logout()

    def test_upload_post(self):
        self.login_first_user()
        response = self.client.get('/upload/')
        first_image = SimpleUploadedFile(name='django.png', content=open(first_image_path, 'rb').read(), content_type='image/png')
        caption = 'Batman vs Superman'
        post = Post.objects.create(username=response.context['user'], image=first_image, caption=caption, upload_time=datetime.datetime.now())
        response = self.client.get('/post/', {'post_id': post.id})
        page = response.content.decode('utf8') 
        self.assertIn(caption, page)
        self.client.logout()
        return post
    
    def test_follow(self):
        post = self.test_upload_post()
        self.login_second_user()
        response = self.client.get('/profile/')
        Follow.objects.create(username=response.context['user'], following=first_user['username'])
        response = self.client.get('/feed/')
        page = response.content.decode('utf8') 
        self.assertIn(first_user['username'], page)
        self.client.logout()
        return post
    
    def test_comment(self):
        post = self.test_follow()
        self.login_second_user(create=False)
        response = self.client.get('/post/', {'post_id': post.id})
        page = response.content.decode('utf8')
        self.assertIn(post.caption, page)
        comment = 'I will destroy you.'
        Comment.objects.create(username=response.context['user'], comment=comment, upload_time=datetime.datetime.now(), post_key=post.id)
        response = self.client.get('/post/', {'post_id': post.id})
        page = response.content.decode('utf8')
        self.assertIn(comment, page)
        self.client.logout()

    def test_like(self):
        post = self.test_follow()
        self.login_first_user(create=False)
        response = self.client.get('/post/', {'post_id': post.id})
        Like.objects.create(username=first_user['username'], post_key=post.id)
        response = self.client.get('/post/', {'post_id': post.id})
        page = response.content.decode('utf-8')
        self.assertIn("liked.png", page)
        self.client.logout()
