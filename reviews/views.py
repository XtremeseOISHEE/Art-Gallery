# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Review, ReviewLike, ReviewComment
# from artworks.models import Artwork
# from .forms import ReviewForm, ReviewCommentForm
# from orders.models import Order

# @login_required
# def create_review(request, artwork_id):
#     artwork = get_object_or_404(Artwork, id=artwork_id)

#     if Review.objects.filter(artwork=artwork, user=request.user).exists():
#         return redirect('artwork_detail', pk=artwork_id)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.artwork = artwork
#             review.user = request.user
#             review.is_verified_purchase = Order.objects.filter(
#                 user=request.user, artwork=artwork, status='completed'
#             ).exists()
#             review.save()
#             return redirect('artwork_detail', pk=artwork_id)
#     else:
#         form = ReviewForm()

#     return render(request, 'reviews/create_review.html', {'form': form, 'artwork': artwork})

# @login_required
# def like_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id)

#     like, created = ReviewLike.objects.get_or_create(
#         review=review,
#         user=request.user,
#         defaults={'is_like': True}   # IMPORTANT: default value set directly
#     )

#     if not created:
#         # Toggle the is_like value
#         like.is_like = not like.is_like
#         like.save()

#     return redirect('artwork_detail', pk=review.artwork.id)

# @login_required
# def add_comment(request, review_id):
#     review = get_object_or_404(Review, id=review_id)

#     if request.method == 'POST':
#         form = ReviewCommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.review = review
#             comment.user = request.user
#             comment.save()
#             return redirect('artwork_detail', pk=review.artwork.id)
#     else:
#         form = ReviewCommentForm()

#     return render(request, 'reviews/add_comment.html', {'form': form, 'review': review})

# @login_required
# def delete_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id)

#     if request.user == review.user or request.user.is_staff:
#         review.delete()

#     return redirect('artwork_detail', pk=review.artwork.id)


# from .forms import ReviewEditForm, CommentEditForm

# # Edit review view
# def edit_review(request, pk):
#     review = get_object_or_404(Review, pk=pk)
#     if request.method == 'POST':
#         form = ReviewEditForm(request.POST, instance=review)
#         if form.is_valid():
#             form.save()
#             return redirect('review_detail', pk=review.pk)  # Redirect to the review detail page
#     else:
#         form = ReviewEditForm(instance=review)
#     return render(request, 'artworks/edit_review.html', {'form': form})

# # Edit comment view
# def edit_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     if request.method == 'POST':
#         form = CommentEditForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('review_detail', pk=comment.review.pk)  # Redirect to the review detail page
#     else:
#         form = CommentEditForm(instance=comment)
#     return render(request, 'artworks/edit_comment.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Review, ReviewLike, ReviewComment
from artworks.models import Artwork
from .forms import ReviewForm, ReviewCommentForm
from orders.models import Order

# Create a review
@login_required
def create_review(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

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

# Like or Dislike a review
@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    like, created = ReviewLike.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'is_like': True}
    )

    if not created:
        like.is_like = not like.is_like
        like.save()

    return redirect('artwork_detail', pk=review.artwork.id)

# Add a comment to a review
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
    else:
        form = ReviewCommentForm()

    return render(request, 'reviews/add_comment.html', {'form': form, 'review': review})

# Delete a review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user == review.user or request.user.is_staff:
        review.delete()

    return redirect('artwork_detail', pk=review.artwork.id)

# Edit a review
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('artwork_detail', pk=review.artwork.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})

# Edit a comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(ReviewComment, pk=comment_id)

    if request.user != comment.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this comment.")

    if request.method == 'POST':
        form = ReviewCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('artwork_detail', pk=comment.review.artwork.id)
    else:
        form = ReviewCommentForm(instance=comment)

    return render(request, 'reviews/edit_comment.html', {'form': form, 'comment': comment})

from django.http import HttpResponseForbidden

# @login_required
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(ReviewComment, id=comment_id)

#     # Check if the logged-in user is the owner of the comment or admin
#     if request.user == comment.user or request.user.is_staff:
#         review_id = comment.review.id  # Store the review id before deleting
#         comment.delete()
#         return redirect('artwork_detail', pk=review_id)
#     else:
#         return HttpResponseForbidden("You do not have permission to delete this comment.")


@login_required
def delete_comment(request, comment_id):
    # Get the comment object
    comment = get_object_or_404(ReviewComment, id=comment_id)

    # Check if the logged-in user is the owner of the comment or an admin
    if request.user == comment.user or request.user.is_staff:
        review_id = comment.review.id  # Store the review id before deleting
        comment.delete()
        return redirect('artwork_detail', pk=review_id)
    else:
        return HttpResponseForbidden("You do not have permission to delete this comment.")
