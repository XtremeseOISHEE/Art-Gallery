from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork
from .forms import ArtworkForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
# Artwork Details
from django.contrib import messages


from .models import Artwork, CATEGORY_CHOICES, ART_TYPE_CHOICES


def homepage(request):
    return render(request, 'artworks/home.html')

def is_staff(user):
    return user.is_staff

# Create Artwork
@login_required
def artwork_create(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user
            artwork.save()
            return redirect('artwork_detail', pk=artwork.pk)
    else:
        form = ArtworkForm()
    return render(request, 'artworks/artwork_form.html', {'form': form})

# Edit Artwork
@login_required
def artwork_edit(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.user != artwork.artist:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('artwork_detail', pk=artwork.pk)
    else:
        form = ArtworkForm(instance=artwork)
    return render(request, 'artworks/artwork_form.html', {'form': form})

# Delete Artwork
@login_required
def artwork_delete(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.user != artwork.artist:
        return HttpResponseForbidden()

    if request.method == 'POST':
        artwork.delete()
        return redirect('artwork_list')
    return render(request, 'artworks/artwork_confirm_delete.html', {'artwork': artwork})

# List Artworks

def artwork_list(request):
    query = request.GET.get('q')  # Search box theke query nicchi
    category = request.GET.get('category', '')
    art_type = request.GET.get('art_type', '')

    filters = Q(is_available=True, is_approved=True)

    if query:
        filters &= (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(art_type__icontains=query)
        )

    if category:
        filters &= Q(category=category)

    if art_type:
        filters &= Q(art_type=art_type)

    artworks = Artwork.objects.filter(filters)

    category_choices = CATEGORY_CHOICES  # Make sure you have these choices in your model or somewhere
    art_type_choices = ART_TYPE_CHOICES  # Make sure you have these choices in your model or somewhere

    return render(request, 'artworks/artwork_list.html', {
        'artworks': artworks,
        'query': query,
        'category': category,
        'art_type': art_type,
        'category_choices': category_choices,
        'art_type_choices': art_type_choices
    })



# Artwork Details
def artwork_detail(request, pk):
    artwork = Artwork.objects.filter(pk=pk).first()
    
    if artwork is None:
        return render(request, '404.html', status=404)  # Custom 404 if artwork not found

    if not artwork.is_approved:
        messages.info(request, "Your artwork is pending approval. We will notify you once it's approved.")
        return redirect('artwork_list')  # Redirect to artwork browsing page

    # Approved artwork: increase view count
    artwork.views += 1
    artwork.save()

    return render(request, 'artworks/artwork_detail.html', {'artwork': artwork})

# Approve Artwork (staff only)

@user_passes_test(is_staff)
def artwork_approve(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    
    # Check if artwork is already approved
    if artwork.is_approved:
        return redirect('artwork_detail', pk=artwork.pk)  # Redirect if already approved
    
    # Approve the artwork
    artwork.is_approved = True
    artwork.save()
    
    return redirect('artwork_detail', pk=artwork.pk)
# Search Artworks
# views.py

def artwork_search(request):
    query = request.GET.get('q')
    category = request.GET.get('category', '')
    art_type = request.GET.get('art_type', '')

    filters = Q()

    if query:
        filters &= (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(art_type__icontains=query)
        )

    if category:
        filters &= Q(category=category)

    if art_type:
        filters &= Q(art_type=art_type)

    artworks = Artwork.objects.filter(filters)

    category_choices = CATEGORY_CHOICES  # Pass category choices to the template
    art_type_choices = ART_TYPE_CHOICES  # Pass art type choices to the template

    return render(request, 'artworks/artwork_list.html', {
        'artworks': artworks,
        'query': query,
        'category': category,
        'art_type': art_type,
        'category_choices': category_choices,
        'art_type_choices': art_type_choices
    })
