from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .forms import UserRegisterForm

# Create your tests here.
class UserRegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com'
        }
        self.invalid_data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'differentpassword',
            'email': 'testuser@example.com'
        }
        
    def test_user_register_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_shop_ecommerce/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)
        
    def test_user_register_post_valid(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.cookies.get('sessionid'))