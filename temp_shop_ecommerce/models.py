from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

# Create your models here.

class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        
        if creating:
            OrderSummary.objects.create(
                client=self,
                total_price=0,
                address='Address',
                city='City',
                phone_number='Phone Number'
            )

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stored_quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#deprecieted
#class Client(models.Model):
#    name = models.CharField(max_length=255)
#    surname = models.CharField(max_length=255)
#    login = models.CharField(max_length=20)
#    email = models.CharField(max_length=30)
#    password = models.CharField(max_length=30)

class OrderSummary(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_summary = models.ForeignKey(OrderSummary, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stored_quantity:
            raise ValueError('Not enough quantity in stock')

        with transaction.atomic():
            self.product.stored_quantity -= self.quantity
            self.product.save(update_fields=['stored_quantity'])
            super().save(*args, **kwargs)
            
    def delete(self, *args, **kwargs):
        order_price = self.quantity * self.product.price
        
        with transaction.atomic():
            self.order_summary.total_price -= order_price
            self.product.stored_quantity += self.quantity
            self.order_summary.save(update_fields=['total_price'])
            super().delete(*args, **kwargs)