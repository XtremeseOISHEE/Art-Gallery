# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from .models import Notification
# from artworks.models import Artwork
# from orders.models import Order
# from reviews.models import Review, ReviewComment, ReviewLike
# from django.contrib.auth import get_user_model

# User = get_user_model()

# # 1. Artwork created → Admin notified
# @receiver(post_save, sender=Artwork)
# def notify_artwork_created(sender, instance, created, **kwargs):
#     if created:
#         admins = User.objects.filter(is_superuser=True)
#         for admin in admins:
#             Notification.objects.create(
#                 recipient=admin,
#                 actor=instance.artist,
#                 verb='submitted a new artwork',
#                 target=instance.title
#             )

# # 2. Artwork approved/unapproved → Seller notified
# @receiver(post_save, sender=Artwork)
# def notify_artwork_approval(sender, instance, created, **kwargs):
#     if not created:
#         Notification.objects.create(
#             recipient=instance.artist,
#             actor=None,
#             verb='Your artwork was approved' if instance.is_approved else 'Your artwork was unapproved',
#             target=instance.title
#         )

# # 3. Order placed → Seller + Admin notified
# @receiver(post_save, sender=Order)
# def notify_order_created(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.buyer,
#             verb='ordered your artwork',
#             target=instance.artwork.title
#         )
#         admins = User.objects.filter(is_superuser=True)
#         for admin in admins:
#             Notification.objects.create(
#                 recipient=admin,
#                 actor=instance.buyer,
#                 verb='placed a new order',
#                 target=instance.artwork.title
#             )

# # 4. Order confirmed/rejected → Buyer notified
# @receiver(post_save, sender=Order)
# def notify_order_status_change(sender, instance, created, **kwargs):
#     if not created:
#         if instance.status == 'confirmed':
#             Notification.objects.create(
#                 recipient=instance.buyer,
#                 actor=instance.artwork.artist,
#                 verb='confirmed your order',
#                 target=instance.artwork.title
#             )
#         elif instance.status == 'rejected':
#             Notification.objects.create(
#                 recipient=instance.buyer,
#                 actor=instance.artwork.artist,
#                 verb='rejected your order',
#                 target=instance.artwork.title
#             )

# # 5. Review created → Artwork owner notified
# @receiver(post_save, sender=Review)
# def notify_review_added(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,  # <-- use the correct field name here
#             verb='reviewed your artwork',
#             target=instance.artwork.title
#         )


# # 6. Review Like → Review author notified
# @receiver(post_save, sender=ReviewLike)
# def notify_review_liked(sender, instance, created, **kwargs):
#     if created and instance.user != instance.review.author:
#         Notification.objects.create(
#             recipient=instance.review.author,
#             actor=instance.user,
#             verb='liked your review',
#             target=instance.review.artwork.title
#         )
# @receiver(post_save, sender=ReviewComment)
# def notify_review_commented(sender, instance, created, **kwargs):
#     if created and instance.user != instance.review.user:
#         Notification.objects.create(
#             recipient=instance.review.user,
#             actor=instance.user,
#             verb='commented on your review',
#             target=instance.review.artwork.title
#         )


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Notification
from artworks.models import Artwork
from orders.models import Order
from reviews.models import Review, ReviewLike
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. Artwork created → Admin notified
@receiver(post_save, sender=Artwork)
def notify_artwork_created(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                actor=instance.artist,
                verb='submitted a new artwork',
                target=instance.title
            )

# 2. Artwork approval changed → Seller notified
@receiver(post_save, sender=Artwork)
def notify_artwork_approval_change(sender, instance, created, **kwargs):
    if not created:
        try:
            previous = Artwork.objects.get(pk=instance.pk)
        except Artwork.DoesNotExist:
            return  # Just in case object is missing (very rare)

        if previous.is_approved != instance.is_approved:
            system_user = User.objects.filter(is_superuser=True).first()
            Notification.objects.create(
                recipient=instance.artist,
                actor=system_user,
                verb='Your artwork was approved' if instance.is_approved else 'Your artwork was unapproved',
                target=instance.title
            )

# 3. Order created → Seller + Admin notified
@receiver(post_save, sender=Order)
def notify_order_created(sender, instance, created, **kwargs):
    if created:
        # Notify seller
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='ordered your artwork',
            target=instance.artwork.title
        )
        # Notify admin
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                actor=instance.user,
                verb='placed a new order',
                target=instance.artwork.title
            )

# 4. Order status changed → Buyer notified
@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    if not created:
        try:
            previous = Order.objects.get(pk=instance.pk)
        except Order.DoesNotExist:
            return

        if previous.status != instance.status:
            if instance.status == 'confirmed':
                Notification.objects.create(
                    recipient=instance.user,
                    actor=instance.artwork.artist,
                    verb='confirmed your order',
                    target=instance.artwork.title
                )
            elif instance.status == 'rejected':
                Notification.objects.create(
                    recipient=instance.user,
                    actor=instance.artwork.artist,
                    verb='rejected your order',
                    target=instance.artwork.title
                )

# 5. Review created → Notify artwork owner
@receiver(post_save, sender=Review)
def notify_review_added(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='reviewed your artwork',
            target=instance.artwork.title
        )

# 6. Review liked → Notify review author
@receiver(post_save, sender=ReviewLike)
def notify_review_liked(sender, instance, created, **kwargs):
    review_author = instance.review.user
    if created and instance.user != review_author:
        Notification.objects.create(
            recipient=review_author,
            actor=instance.user,
            verb='liked your review',
            target=instance.review.artwork.title
        )

from artworks.models import ArtworkLike, ArtworkComment

# 7. Artwork liked → Notify artist
@receiver(post_save, sender=ArtworkLike)
def notify_artwork_liked(sender, instance, created, **kwargs):
    if created and instance.user != instance.artwork.artist:
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='liked your artwork',
            target=instance.artwork.title
        )

# 8. Artwork commented → Notify artist
@receiver(post_save, sender=ArtworkComment)
def notify_artwork_commented(sender, instance, created, **kwargs):
    if created and instance.user != instance.artwork.artist:
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='commented on your artwork',
            target=instance.artwork.title
        )
