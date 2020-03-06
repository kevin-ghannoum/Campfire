from django.test import TestCase, Client

# Create your tests here.
class test(TestCase):
    def test(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(response.status_code, 200)
