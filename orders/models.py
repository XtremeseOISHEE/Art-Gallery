from django.db import models

# Create your models here.

from django.conf import settings
from artworks.models import Artwork  # Import Artwork model from artworks app

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    # near other fields
    is_paid = models.BooleanField(default=False)
    # in orders/models.py
    delivery_name = models.CharField(max_length=100, blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField(blank=True)

    # Fields for refund
    is_refunded = models.BooleanField(default=False) # eta diye refund request krse kina check hy but refund approved kina etar jnne na
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    REFUND_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    refund_status = models.CharField(max_length=10, choices=REFUND_CHOICES, default='pending')
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.artwork.title} x {self.quantity}"
    
    def get_total_price(self):
        return self.artwork.price * self.quantity
 