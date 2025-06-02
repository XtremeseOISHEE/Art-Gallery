from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, LoginForm
# users/views.py
from django.shortcuts import render, get_object_or_404
from .models import User
from django.contrib.auth.decorators import user_passes_test



def staff_or_admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and (u.is_superuser or u.role == 'staff')
    )(view_func)
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



from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from artworks.models import Artwork
from orders.models import Order
from django.db.models import Avg
from users.models import User


def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = getattr(profile_user, 'userprofile', None)

    total_artworks = Artwork.objects.filter(artist=profile_user).count()
    total_sales = Order.objects.filter(artwork__artist=profile_user).count()
    avg_rating = profile_user.review_set.aggregate(Avg('rating'))['rating__avg']

    recent_artworks = Artwork.objects.filter(artist=profile_user).order_by('-created_at')[:3]

    is_owner = request.user == profile_user

    return render(request, 'users/user_profile.html', {
        'user': profile_user,
        'profile': profile,
        'total_artworks': total_artworks,
        'total_sales': total_sales,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'recent_artworks': recent_artworks,
        'is_owner': is_owner,
    })


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
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=request.user.username)

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
    #return redirect('view_profile', username=request.user.username)

