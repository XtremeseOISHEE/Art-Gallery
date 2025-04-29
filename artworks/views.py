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
# def artwork_detail(request, pk):
#     artwork = Artwork.objects.filter(pk=pk).first()
    
#     if artwork is None:
#         return render(request, '404.html', status=404)  # Custom 404 if artwork not found

#     if not artwork.is_approved:
#         messages.info(request, "Your artwork is pending approval. We will notify you once it's approved.")
#         return redirect('artwork_list')  # Redirect to artwork browsing page

#     # Approved artwork: increase view count
#     artwork.views += 1
#     artwork.save()

#     return render(request, 'artworks/artwork_detail.html', {'artwork': artwork})

# from django.contrib.auth.decorators import login_required
# from django.db.models import Count
# from django.contrib import messages
# from django.shortcuts import render, redirect, get_object_or_404
# from reviews.forms import ReviewForm

# @login_required
# def artwork_detail(request, pk):
#     # Retrieve the artwork or return a 404 if not found
#     artwork = get_object_or_404(Artwork, pk=pk)

#     # Check if the artwork is approved
#     if not artwork.is_approved:
#         messages.info(request, "Your artwork is pending approval. We will notify you once it's approved.")
#         return redirect('artwork_list')

#     # Approved artwork: increase view count
#     artwork.views += 1
#     artwork.save()

#     # Determine whether to show the order button based on the user's role
#     show_order_button = request.user.role in ['buyer', 'seller']

#     order_count = None
#     all_orders_count = None

#     # Seller order count
#     if request.user.role == 'seller' and artwork.artist == request.user:
#         order_count = artwork.order_set.count()

#     # Staff order counts
#     if request.user.role == 'staff':
#         all_orders_count = Artwork.objects.annotate(order_count=Count('order')).values('title', 'order_count')

#     # Prepare likes for reviews
#     user_likes = {}
#     if request.user.is_authenticated:
#         for review in artwork.reviews.all():
#             like = review.likes.filter(user=request.user).first()
#             if like:
#                 user_likes[review.id] = like.is_like

#     # Render page
#     return render(request, 'artworks/artwork_detail.html', {
#         'artwork': artwork,
#         'show_order_button': show_order_button,
#         'order_count': order_count,
#         'all_orders_count': all_orders_count,
#         'form': ReviewForm(),  # Assuming you have a form
#         'user_likes': user_likes,
#     })
# # Approve Artwork (staff only)

# @user_passes_test(is_staff)
# def artwork_approve(request, pk):
#     artwork = get_object_or_404(Artwork, pk=pk)
    
#     # Check if artwork is already approved
#     if artwork.is_approved:
#         return redirect('artwork_detail', pk=artwork.pk)  # Redirect if already approved
    
#     # Approve the artwork
#     artwork.is_approved = True
#     artwork.save()
    
#     return redirect('artwork_detail', pk=artwork.pk)
# # Search Artworks
# # views.py


from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import ReviewForm, ReviewCommentForm  # Add ReviewCommentForm if needed
from artworks.models import Artwork
from reviews.models import Review, ReviewLike, ReviewComment

@login_required
def artwork_detail(request, pk):
    # Retrieve the artwork
    artwork = get_object_or_404(Artwork, pk=pk)

    # Check if the artwork is approved
    if not artwork.is_approved:
        messages.info(request, "Your artwork is pending approval. We will notify you once it's approved.")
        return redirect('artwork_list')

    # Approved artwork: increase view count
    artwork.views += 1
    artwork.save()

    # Determine whether to show the order button
    show_order_button = request.user.role in ['buyer', 'seller']

    order_count = None
    all_orders_count = None

    # Seller order count
    if request.user.role == 'seller' and artwork.artist == request.user:
        order_count = artwork.order_set.count()

    # Staff order counts
    if request.user.role == 'staff':
        all_orders_count = Artwork.objects.annotate(order_count=Count('order')).values('title', 'order_count')

    # Get all reviews for the artwork
    reviews = artwork.reviews.all()

    # Prepare likes and dislikes counts + user like/dislike status
    user_likes = {}
    for review in reviews:
        review.likes_count = review.likes.filter(is_like=True).count()
        review.dislikes_count = review.likes.filter(is_like=False).count()

        # Check if the current user has liked or disliked
        like = review.likes.filter(user=request.user).first()
        if like:
            user_likes[review.id] = like.is_like

    # Render the page
    context = {
        'artwork': artwork,
        'show_order_button': show_order_button,
        'order_count': order_count,
        'all_orders_count': all_orders_count,
        'reviews': reviews,  # pass reviews manually
        'form': ReviewForm(),  # form for adding a review
        'user_likes': user_likes,
    }

    return render(request, 'artworks/artwork_detail.html', context)


@user_passes_test(lambda u: u.is_staff)
def artwork_approve(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    if artwork.is_approved:
        return redirect('artwork_detail', pk=artwork.pk)

    artwork.is_approved = True
    artwork.save()

    return redirect('artwork_detail', pk=artwork.pk)

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
# artworks/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Artwork
from orders.models import Order

@login_required
def my_artworks(request):
    artworks = Artwork.objects.filter(artist=request.user)
    artworks_with_orders = []

    for artwork in artworks:
        orders = Order.objects.filter(artwork=artwork)
        artworks_with_orders.append({
            'artwork': artwork,
            'orders': orders
        })

    return render(request, 'artworks/my_artworks.html', {
        'artworks_with_orders': artworks_with_orders
    })


from django.shortcuts import render

def homepage(request):
    return render(request, 'artworks/home.html')



def is_staff(user):
    return user.is_staff

# View to list all pending artworks
@user_passes_test(is_staff)
def pending_artworks(request):
    pending_arts = Artwork.objects.filter(is_approved=False)
    return render(request, 'artworks/pending_artworks.html', {'pending_arts': pending_arts})

# View to approve a specific artwork
# @user_passes_test(is_staff)
# def artwork_approve(request, pk):
#     artwork = get_object_or_404(Artwork, pk=pk)
    
#     # Check if artwork is already approved
#     if artwork.is_approved:
#         return redirect('artwork_detail', pk=artwork.pk)  # Redirect if already approved
    
#     # Approve the artwork
#     artwork.is_approved = True
#     artwork.save()
    
#     return redirect('pending_artworks')  # Redirect to the pending artworks page after approving
