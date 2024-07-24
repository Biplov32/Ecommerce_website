from django.contrib import admin
from . import views
from base.models import product,Category,ShoppingCart,DeliveryAddress
# Register your models here.
admin.site.register(product)
admin.site.register(Category)
admin.site.register(ShoppingCart)
admin.site.register(DeliveryAddress)