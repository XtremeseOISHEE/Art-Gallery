# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.conf import settings


# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#         ('staff', 'Staff'),
#     )
#     full_name = models.CharField(max_length=100)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     address = models.TextField(blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     # Onno info jodi lage add korte paro

#     def __str__(self):
#         return self.user.username

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('staff', 'Staff'),
    )
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Address Info
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Contact Info
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Bio
    bio = models.TextField(blank=True, null=True)

    # Social Links
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
