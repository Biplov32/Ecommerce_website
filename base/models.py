from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name =models.CharField(max_length=255)

    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    photo = models.FileField(upload_to='uploads/')

class ShoppingCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product =models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} - {self.product.name} x {self.quantity}'