from django.test import TestCase, Client
from django.contrib.auth.models import User

first_user = {'username': 'Batman', 'password': 'Wayne8'}
second_user = {'username': 'Spiderman', 'password': 'Parker4'}

# Create your tests here.
class Test(TestCase):
    def login_first_user(self):
        User.objects.create_user(username=first_user['username'], password=first_user['password'])
        self.client.login(username=first_user['username'], password=first_user['password'])
    
    def login_second_user(self):
        User.objects.create_user(username=second_user['username'], password=second_user['password'])
        self.client.login(username=second_user['username'], password=second_user['password'])
    
    def test_create_users(self):
        self.login_first_user()
        self.client.logout()
        self.login_second_user()
        self.client.logout()
    
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
