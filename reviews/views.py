from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review, ReviewLike, ReviewComment
from artworks.models import Artwork
from .forms import ReviewForm, ReviewCommentForm
from orders.models import Order

@login_required
def create_review(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    # Check if user already reviewed this artwork
    if Review.objects.filter(artwork=artwork, user=request.user).exists():
        return redirect('artwork_detail', pk=artwork_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.artwork = artwork
            review.user = request.user
            review.is_verified_purchase = Order.objects.filter(
                user=request.user, artwork=artwork, status='completed'
            ).exists()
            review.save()
            return redirect('artwork_detail', pk=artwork_id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'form': form, 'artwork': artwork})

@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(review=review, user=request.user)

    if not created:
        like.is_like = not like.is_like
        like.save()

    return redirect('artwork_detail', pk=review.artwork.id)

@login_required
def add_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()

    return redirect('artwork_detail', pk=review.artwork.id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Allow either the review owner or staff to delete
    if request.user == review.user or request.user.is_staff:
        review.delete()

    return redirect('artwork_detail', pk=review.artwork.id)
