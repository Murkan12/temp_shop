from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from ..forms import UserRegisterForm
from ..models import Product, Order, OrderSummary

User = get_user_model()

class EcomRegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.template_name = 'temp_shop_ecommerce/register.html'
        self.valid_data = {
            'username': 'testuser',
            'password1': 'password123%',
            'password2': 'password123%',
            'email': 'testuser@example.com'
        }
        self.invalid_data = {
            'username': 'testuser',
            'password1': 'password123%',
            'password2': 'differentpassword',
            'email': 'testuser@example.com'
        }
    
    def test_register_view_get(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], UserRegisterForm)
        
    def test_register_view_post_invalid(self):
        response = self.client.post(self.url, self.invalid_data)
        
        # The view returns the form again but with error messages
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, self.template_name)
        
        self.assertTrue(response.context['form'].errors)
        
    def test_register_view_post_valid(self):
        response = self.client.post(self.url, self.valid_data)
        
        # Checking if the response is a redirect
        self.assertEqual(response.status_code, 302)        
        self.assertRedirects(response, reverse('email_confirmation_sent'))
        
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('User account activation', mail.outbox[0].subject)

class EcomLoginViewTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test', email='test@email.com', password='test1234%')
        self.valid_data = {
            'username': user.username,
            'password': user.password
        }
        self.invalid_username = {
            'username': 'cos',
            'password': user.password
        }
        self.invalid_password = {
            'username': user.username,
            'password': 'cos'
        }
        
        self.url = reverse('login')
        self.template_name = 'temp_shop_ecommerce/login.html'
        
    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        
    def test_login_post_invalid_username(self):
        response = self.client.post(self.url, self.invalid_username)
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context['form'].errors)
        
    def test_login_post_invalid_password(self):
        response = self.client.post(self.url, self.invalid_password)
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context['form'].errors)
        
    def test_login_post_valid(self):
        response = self.client.post(self.url, self.valid_data)
        print(response.context['form'].errors)

class EcomCreateOrderViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='test1234564', email='test@email.com')
        self.product = Product.objects.create(name='TEST1', description='TEST1 ITEM', price=10, stored_quantity=100, category='item')
        
        self.client.login(username='test', password='test1234564')
        
        self.valid_data = {
            'user': self.user
        }
        
    #def test_create_order_post(self):
        #response = self.client.post(f'/ecommerce/create_order/{self.product.pk}/', self.valid_data)
        #self.assertNotEqual(response.status_code, 404)
        
        #order_summary = OrderSummary.objects.get(client=self.user)
        #self.assertIsNotNone(order_summary)
        
        #order = Order.objects.get(order_summary=order_summary, product=self.product)
        #self.assertIsNotNone(order)
        
        #self.assertRedirects(response, '/ecommerce/')
        