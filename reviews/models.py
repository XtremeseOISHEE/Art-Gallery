from django.db import models
from django.conf import settings
from artworks.models import Artwork

class Review(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified_purchase = models.BooleanField(default=False)

    class Meta:
        unique_together = ('artwork', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.artwork.title} reviewed by {self.user.username}"

class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True = Like, False = Dislike
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user.username} {'liked' if self.is_like else 'disliked'} review {self.review.id}"

class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on review {self.review.id}"
