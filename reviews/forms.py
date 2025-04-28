from django import forms
from .models import Review, ReviewComment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2}),
        }
