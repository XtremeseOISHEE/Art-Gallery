from django.contrib import admin

# Register your models here.

from .models import Order, Cart, CartItem

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
