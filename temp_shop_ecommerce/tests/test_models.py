from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from ..models import Product, Order, OrderSummary

class EcomModelsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_case_user', password='Viktorek1', email='example@gmail.com')
        product = Product.objects.create(name='T-shirt', description='A cotton t-shirt',
                               price=59.99, stored_quantity=10000)
        order_summary = OrderSummary.objects.get(client=user)
        Order.objects.create(product=product, order_summary=order_summary, quantity=1)
        
    def test_model_creation(self):
        user = User.objects.get(username='test_case_user')
        product = Product.objects.get(name='T-shirt')
        order_summary = OrderSummary.objects.get(client=user)
        order = Order.objects.get(product=product)
        
        self.assertIsNotNone(user)
        self.assertIsNotNone(product)
        self.assertIsNotNone(order_summary)
        self.assertIsNotNone(order)