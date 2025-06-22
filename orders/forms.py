# from django import forms
# from .models import Order
# from artworks.models import Artwork  # Import Artwork model to validate

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['quantity']  # Only need quantity for now since artwork is selected by URL

#     def __init__(self, *args, **kwargs):
#         self.artwork = kwargs.pop('artwork', None)
#         super(OrderForm, self).__init__(*args, **kwargs)
#         if self.artwork:
#             self.fields['quantity'].widget.attrs.update({'min': 1, 'max': self.artwork.stock})  # Set max quantity based on stock

#     def clean_quantity(self):
#         quantity = self.cleaned_data.get('quantity')
#         if quantity <= 0:
#             raise forms.ValidationError("Quantity must be greater than 0.")
#         return quantity

from django import forms
from .models import Order
from artworks.models import Artwork  # Import Artwork model to validate

class OrderForm(forms.ModelForm):
    # Optional dynamic fields
    size = forms.ChoiceField(choices=[], required=False)
    frame = forms.ChoiceField(
        choices=[
            ('none', 'No Frame'),
            ('wood', 'Wood Frame (+৳300)'),
            ('metal', 'Metal Frame (+৳350)'),
            ('acrylic', 'Acrylic Frame (+৳250)')
        ],
        required=False
    )

    class Meta:
        model = Order
        fields = ['quantity', 'size', 'frame']  # ✅ field name is quantity, not amount or quanity

    def __init__(self, *args, **kwargs):
        self.artwork = kwargs.pop('artwork', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        if self.artwork:
            self.fields['quantity'].widget.attrs.update({'min': 1})

            # Dynamically set size choices based on artwork type
            if self.artwork.art_type in ['digital', 'illustration']:
                self.fields['size'].choices = [
                    ('1080x1350', '1080×1350 px'),
                    ('1080x1080', '1080×1080 px'),
                    ('1920x1080', '1920×1080 px'),
                    ('3508x4961', '3508×4961 px'),
                ]
            elif self.artwork.art_type in ['poster', 'traditional', 'exclusive_paintings', 'print']:
                self.fields['size'].choices = [
                    ('A4', 'A4 (8.3×11.7 in)'),
                    ('A3', 'A3 (11.7×16.5 in)'),
                    ('A2', 'A2 (16.5×23.4 in)'),
                    ('A1', 'A1 (23.4×33.1 in)'),
                    ('18x24', '18×24 in'),
                    ('24x36', '24×36 in'),
                ]
            else:
                self.fields['size'].choices = []

            # Remove frame if not applicable
            if self.artwork.art_type not in ['poster', 'traditional', 'exclusive_paintings', 'print']:
                self.fields.pop('frame', None)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity

