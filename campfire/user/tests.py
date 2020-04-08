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
