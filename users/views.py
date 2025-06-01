from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, get_object_or_404
from .models import User

# Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to homepage after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage after login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

# Logout View
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the homepage or any other page



def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'userprofile', None)
    return render(request, 'users/view_profile.html', {'profile': profile, 'user_obj': user})


from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm  # niche form example dilam
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def edit_profile(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
