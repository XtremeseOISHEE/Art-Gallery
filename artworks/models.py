from django.db import models
from django.conf import settings


# 
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# 

CATEGORY_CHOICES = [
    ('abstract', 'Abstract'),
    ('landscape', 'Landscape'),
    ('portrait', 'Portrait'),
    ('fantasy', 'Fantasy'),
    ('food', 'Food'),
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
    ('illustration', 'Illustration'),
    ('poster', 'Poster'),
    ('exclusive_paintings', 'Exclusive Paintings'),
    ('handmade_crafts', 'Handmade Crafts'),
    ('print', 'Print'),
]
# maryam
ART_TYPE_CHOICES = [
    ('traditional', 'Traditional Art'),
    ('photography', 'Photography'),
    ('poster', 'Poster'),
    ('exclusive_paintings', 'Exclusive Paintings'),
    ('print', 'Print'),
    ('digital', 'Digital Art'),
    ('illustration', 'Illustration'),
    ('3d', '3D Art / Sculpting'),
    ('handmade_crafts', 'Handmade Crafts'),
]

SIZE_CHOICES = [
    ('A4', 'A4 (8.3×11.7 in)'),
    ('A3', 'A3 (11.7×16.5 in)'),
    ('A2', 'A2 (16.5×23.4 in)'),
    ('A1', 'A1 (23.4×33.1 in)'),
    ('18x24', '18×24 in'),
    ('24x36', '24×36 in'),
]

PIXEL_SIZE_CHOICES = [
    ('1080x1350', '1080×1350 px'),
    ('1080x1080', '1080×1080 px'),
    ('1920x1080', '1920×1080 px'),
    ('3508x4961', '3508×4961 px (A4 @ 300dpi)'),
]

FRAME_CHOICES = [
    ('none', 'No Frame'),
    ('wood', 'Wood Frame (+৳300)'),
    ('metal', 'Metal Frame (+৳350)'),
    ('acrylic', 'Acrylic Frame (+৳250)'),
]

EXTRA_IMAGES = 4


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
    # maryam
    categories = models.ManyToManyField(Category)
    art_type = models.CharField(max_length=30, choices=ART_TYPE_CHOICES)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True, null=True)
    custom_size = models.CharField(max_length=100, blank=True, null=True)
    frame = models.CharField(max_length=20, choices=FRAME_CHOICES, default='none')

    def __str__(self):
        return self.title

class ArtworkImage(models.Model):
    artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='artworks/extra/')


@property
def average_rating(self):
    reviews = self.reviews.all()
    if reviews:
        return round(sum([review.rating for review in reviews]) / reviews.count(), 2)
    return 0


from django.db import models
from django.conf import settings

class ArtworkLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ArtworkComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
