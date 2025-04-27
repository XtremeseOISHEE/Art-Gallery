from django import forms
from .models import Order
from artworks.models import Artwork  # Import Artwork model to validate

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']  # Only need quantity for now since artwork is selected by URL

    def __init__(self, *args, **kwargs):
        self.artwork = kwargs.pop('artwork', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.artwork:
            self.fields['quantity'].widget.attrs.update({'min': 1, 'max': self.artwork.stock})  # Set max quantity based on stock

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity
