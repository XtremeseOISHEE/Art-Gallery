# from django import forms
# from .models import Review, ReviewComment
# from .models import Review, Comment
# from .models import Review, ReviewComment 

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['rating', 'comment']
#         widgets = {
#             'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
#             'comment': forms.Textarea(attrs={'rows': 3}),
#         }

# class ReviewCommentForm(forms.ModelForm):
#     class Meta:
#         model = ReviewComment
#         fields = ['comment']
#         widgets = {
#             'comment': forms.Textarea(attrs={'rows': 2}),
#         }

# class ReviewEditForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['content', 'rating']

# class CommentEditForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']

from django import forms
from .models import Review, ReviewComment  # Import the required models

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Include the fields you want to capture
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['comment']  # Only the comment field for adding a comment
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']  # Allow editing comment and rating

class ReviewCommentEditForm(forms.ModelForm):  # Correctly named form for editing ReviewComment
    class Meta:
        model = ReviewComment
        fields = ['comment']  # Only the comment field for editing the comment
