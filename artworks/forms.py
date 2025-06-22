from django import forms
from .models import Artwork, ArtworkImage, SIZE_CHOICES, PIXEL_SIZE_CHOICES, EXTRA_IMAGES
from django.forms import modelformset_factory, inlineformset_factory

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'image', 'description', 'price', 'category', 'art_type', 'size', 'custom_size']
        # No need to specify widget for ForeignKey field (category)

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


class ArtworkImageForm(forms.ModelForm):
    class Meta:
        model = ArtworkImage
        fields = ['image']  # no 'multiple' here

ArtworkImageFormSet = inlineformset_factory(
    Artwork, ArtworkImage,
    form=ArtworkImageForm,
    fields=['image'],
    extra=EXTRA_IMAGES,
    max_num=EXTRA_IMAGES,
    validate_max=True,
    can_delete=True
)
