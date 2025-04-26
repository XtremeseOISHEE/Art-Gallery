from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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
