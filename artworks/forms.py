from django import forms
from .models import Artwork
from .models import Artwork, SIZE_CHOICES, PIXEL_SIZE_CHOICES

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
