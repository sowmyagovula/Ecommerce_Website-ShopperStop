from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Shop_model(models.Model):
    CATEGORY_CHOICES = [
        ('makeup', 'Makeup'),
        ('fashion', 'Fashion'),
        ('skincare', 'skincare'),
        ('electronics', 'Electronics'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Makeup'
    )
    brand = models.CharField(max_length=100, default='DefaultBrand')
    product_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    desc = models.TextField(max_length=500)
    image = models.ImageField(upload_to='media/', blank=False, null = False)

    def __str__(self):
        return f"{self.user.username} - {self.brand} - {self.product_name} - {self.desc[:10]}"
    
class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shop_model, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Shop_model, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()