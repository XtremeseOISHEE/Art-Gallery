from django import forms
from .models import Artwork, ArtworkImage, SIZE_CHOICES, PIXEL_SIZE_CHOICES, EXTRA_IMAGES
from django.forms import modelformset_factory, inlineformset_factory

# class ArtworkForm(forms.ModelForm):
#     class Meta:
#         model = Artwork
#         fields = ['title', 'description', 'price', 'image', 'category', 'art_type']

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'image', 'description', 'price', 'categories', 'art_type', 'size', 'custom_size']
        widgets = {
             'categories': forms.SelectMultiple()
        }
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dropdown_types = ['poster', 'traditional', 'print', 'exclusive_paintings']
        pixel_types = ['digital', 'illustration']
        manual_types = ['3d', 'handmade_crafts']

        art_type = self.initial.get('art_type') or self.data.get('art_type')

        if art_type in pixel_types:
            self.fields['size'].choices = PIXEL_SIZE_CHOICES
            self.fields['frame'].widget = forms.HiddenInput()
            self.fields['custom_size'].widget = forms.HiddenInput()
        elif art_type in manual_types:
            self.fields['size'].widget = forms.HiddenInput()
            self.fields['frame'].widget = forms.HiddenInput()
        else:
            self.fields['size'].choices = SIZE_CHOICES
            self.fields['custom_size'].widget = forms.HiddenInput()


# ArtworkImageFormSet = modelformset_factory(
#     ArtworkImage,
#     fields=('image',),
#     extra=EXTRA_IMAGES,  # allow 2 additional images
#     max_num=3
# )

# Optional: Custom ModelForm for ArtworkImage to add 'multiple' attribute to the file input
class ArtworkImageForm(forms.ModelForm):
    class Meta:
        model = ArtworkImage
        fields = ['image']  # don't add 'multiple' here

# Inline formset for up to 4 images
ArtworkImageFormSet = inlineformset_factory(
    Artwork, ArtworkImage,
    form=ArtworkImageForm,            # use the custom form to allow multi-select
    fields=['image'],
    extra=EXTRA_IMAGES,                          # show 4 empty file fields by default
    max_num=EXTRA_IMAGES,                        # hard limit of 4 images
    validate_max=True,                # enforce the max_num limit in validation
    can_delete=True                   # allow removing an image form (optional)
)