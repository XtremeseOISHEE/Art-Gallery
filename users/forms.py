from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import UserProfile

# # Registration Form
# class CustomUserCreationForm(UserCreationForm):
#     full_name = forms.CharField(max_length=100, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'role', 'full_name')


# # Login Form (optional – you can skip this and use POST manually in view)
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['address', 'phone']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


# Registration Form
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'full_name')


# Login Form (optional – you can skip this and use POST manually in view)
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'address',
            'city',
            'state',
            'country',
            'phone',
            'bio',
            'instagram',
            'linkedin',
            'facebook',
            'twitter',
            'website',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
