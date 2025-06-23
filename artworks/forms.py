from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Artwork, ArtworkImage, SIZE_CHOICES, PIXEL_SIZE_CHOICES, EXTRA_IMAGES

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'image', 'description', 'price', 'category', 'art_type', 'size', 'custom_size', 'frame']
        widgets = {
            'category': forms.Select(),
            'size': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pixel_types = ['digital', 'illustration']
        manual_types = ['3d', 'handmade_crafts']

        art_type = self.data.get('art_type') or self.initial.get('art_type')

        if art_type in pixel_types:
            self.fields['size'].choices = PIXEL_SIZE_CHOICES
            self.fields['frame'].widget = forms.HiddenInput()
            self.fields['custom_size'].widget = forms.HiddenInput()
        elif art_type in manual_types:
            self.fields['size'].widget = forms.HiddenInput()
            self.fields['frame'].widget = forms.HiddenInput()
            self.fields['custom_size'].widget = forms.HiddenInput()
        else:
            self.fields['size'].choices = SIZE_CHOICES
            self.fields['custom_size'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        art_type = cleaned_data.get('art_type')
        size = cleaned_data.get('size')

        pixel_types = ['digital', 'illustration']
        manual_types = ['3d', 'handmade_crafts']

        if art_type in pixel_types:
            allowed_sizes = [choice[0] for choice in PIXEL_SIZE_CHOICES]
        elif art_type in manual_types:
            allowed_sizes = []
        else:
            allowed_sizes = [choice[0] for choice in SIZE_CHOICES]

        if size and size not in allowed_sizes:
            raise ValidationError({
                'size': f"Selected size '{size}' is not valid for art type '{art_type}'."
            })

        return cleaned_data

class ArtworkImageForm(forms.ModelForm):
    class Meta:
        model = ArtworkImage
        fields = ['image']

ArtworkImageFormSet = inlineformset_factory(
    Artwork,
    ArtworkImage,
    form=ArtworkImageForm,
    fields=['image'],
    extra=EXTRA_IMAGES,
    max_num=EXTRA_IMAGES,
    validate_max=True,
    can_delete=True,
)
