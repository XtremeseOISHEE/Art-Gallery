from django.contrib import admin
from .models import EXTRA_IMAGES

# Register your models here.

from .models import Artwork, ArtworkImage

class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = EXTRA_IMAGES  # show 2 extra image fields

class ArtworkAdmin(admin.ModelAdmin):
    inlines = [ArtworkImageInline]

admin.site.register(Artwork, ArtworkAdmin)