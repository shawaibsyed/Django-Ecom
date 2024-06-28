from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, editable=False, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"{self.user}"

class Product(models.Model):
    
    product_name = models.CharField(max_length=255, primary_key=True)
    category = models.CharField(max_length=255, null=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, editable=False, related_name='items', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, editable=False, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, editable=False)

    def __str__(self):
        return f"{self.cart} | {self.product_id} | {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name='order')
    price = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, editable=False, on_delete=models.CASCADE, related_name='order_items')
    product_id = models.ForeignKey(Product, editable=False, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, editable=False)
    
