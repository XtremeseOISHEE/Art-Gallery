from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('abstract', 'Abstract'),
    ('landscape', 'Landscape'),
    ('portrait', 'Portrait'),
    ('fantasy', 'Fantasy'),
    ('anime', 'Anime / Manga'),
    ('nature', 'Nature'),
    ('cityscape', 'Cityscape / Urban'),
    ('animals', 'Animals / Wildlife'),
    ('fashion', 'Fashion'),
    ('sports', 'Sports'),
    ('mythology', 'Mythology'),
    ('aesthetic', 'Aesthetic / Minimalism'),
    ('dark_art', 'Dark Art'),
    ('vintage', 'Vintage / Retro'),
    ('surreal', 'Surreal / Dreamy'),
]

ART_TYPE_CHOICES = [
    ('digital', 'Digital Art'),
    ('traditional', 'Traditional Art'),
    ('3d', '3D Art / Sculpting'),
    ('photography', 'Photography'),
    ('fanart', 'Fan Art'),
    ('illustration', 'Illustration'),
    ('concept_art', 'Concept Art'),
    ('pixel_art', 'Pixel Art'),
]

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='artwork/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    art_type = models.CharField(max_length=20, choices=ART_TYPE_CHOICES, default='traditional')
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)  # Track popularity

    def __str__(self):
        return self.title
