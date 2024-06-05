from django.db import models

# Create your models here.
from django.db import models, transaction
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stored_quantity = models.PositiveIntegerField()

#deprecieted
#class Client(models.Model):
#    name = models.CharField(max_length=255)
#    surname = models.CharField(max_length=255)
#    login = models.CharField(max_length=20)
#    email = models.CharField(max_length=30)
#    password = models.CharField(max_length=30)

class OrderSummary(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_summary = models.ForeignKey(OrderSummary, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stored_quantity:
            raise ValueError('Not enough quantity in stock')

        with transaction.atomic():
            self.product.stored_quantity -= self.quantity
            self.product.save(update_fields=['stored_quantity'])
            super().save(*args, **kwargs)