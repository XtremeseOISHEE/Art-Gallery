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


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from .models import Notification
# from artworks.models import Artwork
# from orders.models import Order
# from reviews.models import Review, ReviewLike
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

# # 2. Artwork approval changed → Seller notified
# @receiver(post_save, sender=Artwork)
# def notify_artwork_approval_change(sender, instance, created, **kwargs):
#     if not created:
#         try:
#             previous = Artwork.objects.get(pk=instance.pk)
#         except Artwork.DoesNotExist:
#             return  # Just in case object is missing (very rare)

#         if previous.is_approved != instance.is_approved:
#             system_user = User.objects.filter(is_superuser=True).first()
#             Notification.objects.create(
#                 recipient=instance.artist,
#                 actor=system_user,
#                 verb='Your artwork was approved' if instance.is_approved else 'Your artwork was unapproved',
#                 target=instance.title
#             )

# # 3. Order created → Seller + Admin notified
# @receiver(post_save, sender=Order)
# def notify_order_created(sender, instance, created, **kwargs):
#     if created:
#         # Notify seller
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='ordered your artwork',
#             target=instance.artwork.title
#         )
#         # Notify admin
#         admins = User.objects.filter(is_superuser=True)
#         for admin in admins:
#             Notification.objects.create(
#                 recipient=admin,
#                 actor=instance.user,
#                 verb='placed a new order',
#                 target=instance.artwork.title
#             )

# # 4. Order status changed → Buyer notified
# @receiver(post_save, sender=Order)
# def notify_order_status_change(sender, instance, created, **kwargs):
#     if not created:
#         try:
#             previous = Order.objects.get(pk=instance.pk)
#         except Order.DoesNotExist:
#             return

#         if previous.status != instance.status:
#             if instance.status == 'confirmed':
#                 Notification.objects.create(
#                     recipient=instance.user,
#                     actor=instance.artwork.artist,
#                     verb='confirmed your order',
#                     target=instance.artwork.title
#                 )
#             elif instance.status == 'rejected':
#                 Notification.objects.create(
#                     recipient=instance.user,
#                     actor=instance.artwork.artist,
#                     verb='rejected your order',
#                     target=instance.artwork.title
#                 )

# # 5. Review created → Notify artwork owner
# @receiver(post_save, sender=Review)
# def notify_review_added(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='reviewed your artwork',
#             target=instance.artwork.title
#         )

# # 6. Review liked → Notify review author
# @receiver(post_save, sender=ReviewLike)
# def notify_review_liked(sender, instance, created, **kwargs):
#     review_author = instance.review.user
#     if created and instance.user != review_author:
#         Notification.objects.create(
#             recipient=review_author,
#             actor=instance.user,
#             verb='liked your review',
#             target=instance.review.artwork.title
#         )

# from artworks.models import ArtworkLike, ArtworkComment

# # 7. Artwork liked → Notify artist
# @receiver(post_save, sender=ArtworkLike)
# def notify_artwork_liked(sender, instance, created, **kwargs):
#     if created and instance.user != instance.artwork.artist:
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='liked your artwork',
#             target=instance.artwork.title
#         )

# # 8. Artwork commented → Notify artist
# @receiver(post_save, sender=ArtworkComment)
# def notify_artwork_commented(sender, instance, created, **kwargs):
#     if created and instance.user != instance.artwork.artist:
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='commented on your artwork',
#             target=instance.artwork.title


# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import Notification
# from artworks.models import Artwork, ArtworkLike, ArtworkComment
# from orders.models import Order
# from reviews.models import Review, ReviewLike, ReviewComment

# User = get_user_model()

# # =========== Pre-save to cache old order status and refund status ===========
# @receiver(pre_save, sender=Order)
# def cache_order_old_status(sender, instance, **kwargs):
#     if instance.pk:
#         try:
#             old_order = Order.objects.get(pk=instance.pk)
#             instance._old_status = old_order.status
#             instance._old_refund_status = old_order.refund_status
#             print(f"[pre_save] Cached old status: {instance._old_status}, old refund: {instance._old_refund_status}")
#         except Order.DoesNotExist:
#             instance._old_status = None
#             instance._old_refund_status = None
#             print("[pre_save] Order does not exist, nothing cached")
#     else:
#         instance._old_status = None
#         instance._old_refund_status = None
#         print("[pre_save] New order, no old status")

# # =========== Post-save to notify on order status or refund status change ===========
# @receiver(post_save, sender=Order)
# def notify_order_changes(sender, instance, created, **kwargs):
#     print(f"[post_save] Order saved. Created: {created}, status: {instance.status}, old_status: {getattr(instance, '_old_status', None)}")

#     if created:
#         print("[post_save] Order created, skipping status notification here")
#         return

#     buyer = instance.user
#     seller = instance.artwork.artist
#     admins = User.objects.filter(is_superuser=True)
#     title = instance.artwork.title

#     # Notify buyer on order status change
#     if getattr(instance, '_old_status', None) != instance.status:
#         if instance.status == 'confirmed':
#             print(f"[post_save] Notify buyer {buyer} - order confirmed")
#             Notification.objects.create(
#                 recipient=buyer,
#                 actor=seller,
#                 verb='confirmed your order',
#                 target=title
#             )
#         elif instance.status == 'rejected':
#             print(f"[post_save] Notify buyer {buyer} - order rejected")
#             Notification.objects.create(
#                 recipient=buyer,
#                 actor=seller,
#                 verb='rejected your order',
#                 target=title
#             )

#     # Notify admin/buyer on refund status change
#     if getattr(instance, '_old_refund_status', None) != instance.refund_status:
#         if instance.refund_status == 'requested':
#             print(f"[post_save] Notify admins refund requested by {buyer}")
#             for admin in admins:
#                 Notification.objects.create(
#                     recipient=admin,
#                     actor=buyer,
#                     verb='requested a refund',
#                     target=title
#                 )
#         elif instance.refund_status == 'approved':
#             admin_user = admins.first()
#             print(f"[post_save] Notify buyer {buyer} refund approved")
#             Notification.objects.create(
#                 recipient=buyer,
#                 actor=admin_user,
#                 verb='approved your refund',
#                 target=title
#             )

# # =========== Artwork created → Notify Admins ===========
# @receiver(post_save, sender=Artwork)
# def notify_artwork_created(sender, instance, created, **kwargs):
#     if created:
#         admins = User.objects.filter(is_superuser=True)
#         print(f"[post_save] Artwork created - notifying admins")
#         for admin in admins:
#             Notification.objects.create(
#                 recipient=admin,
#                 actor=instance.artist,
#                 verb='submitted a new artwork',
#                 target=instance.title
#             )

# # =========== Track artwork approval change ===========
# @receiver(pre_save, sender=Artwork)
# def track_artwork_approval_change(sender, instance, **kwargs):
#     if instance.pk:
#         try:
#             old = Artwork.objects.get(pk=instance.pk)
#             instance._approval_changed = (old.is_approved != instance.is_approved)
#             print(f"[pre_save] Artwork approval changed: {instance._approval_changed}")
#         except Artwork.DoesNotExist:
#             instance._approval_changed = False
#     else:
#         instance._approval_changed = False

# # =========== Artwork approval changed → Notify Artist ===========
# @receiver(post_save, sender=Artwork)
# def notify_artwork_approval_change(sender, instance, created, **kwargs):
#     if not created and getattr(instance, '_approval_changed', False):
#         admin_user = User.objects.filter(is_superuser=True).first()
#         print(f"[post_save] Notify artist {instance.artist} about artwork approval change")
#         Notification.objects.create(
#             recipient=instance.artist,
#             actor=admin_user,
#             verb='approved your artwork' if instance.is_approved else 'unapproved your artwork',
#             target=instance.title
#         )

# # =========== Order created → Notify seller and admins ===========
# @receiver(post_save, sender=Order)
# def notify_order_created(sender, instance, created, **kwargs):
#     if created:
#         seller = instance.artwork.artist
#         buyer = instance.user
#         title = instance.artwork.title
#         print(f"[post_save] New order created - notify seller and admins")
#         Notification.objects.create(
#             recipient=seller,
#             actor=buyer,
#             verb='ordered your artwork',
#             target=title
#         )
#         admins = User.objects.filter(is_superuser=True)
#         for admin in admins:
#             Notification.objects.create(
#                 recipient=admin,
#                 actor=buyer,
#                 verb='placed a new order',
#                 target=title
#             )

# # =========== Review created → Notify artwork owner ===========
# @receiver(post_save, sender=Review)
# def notify_review_added(sender, instance, created, **kwargs):
#     if created:
#         print(f"[post_save] New review added - notify artwork owner")
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='reviewed your artwork',
#             target=instance.artwork.title
#         )

# # =========== Review liked → Notify review author ===========
# @receiver(post_save, sender=ReviewLike)
# def notify_review_liked(sender, instance, created, **kwargs):
#     if created and instance.user != instance.review.user:
#         print(f"[post_save] Review liked - notify review author")
#         Notification.objects.create(
#             recipient=instance.review.user,
#             actor=instance.user,
#             verb='liked your review',
#             target=instance.review.artwork.title
#         )

# # =========== Review commented → Notify review author ===========
# @receiver(post_save, sender=ReviewComment)
# def notify_review_commented(sender, instance, created, **kwargs):
#     if created and instance.user != instance.review.user:
#         print(f"[post_save] Review commented - notify review author")
#         Notification.objects.create(
#             recipient=instance.review.user,
#             actor=instance.user,
#             verb='commented on your review',
#             target=instance.review.artwork.title
#         )

# # =========== Artwork liked → Notify artist ===========
# @receiver(post_save, sender=ArtworkLike)
# def notify_artwork_liked(sender, instance, created, **kwargs):
#     if created and instance.user != instance.artwork.artist:
#         print(f"[post_save] Artwork liked - notify artist")
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='liked your artwork',
#             target=instance.artwork.title
#         )

# # =========== Artwork commented → Notify artist ===========
# @receiver(post_save, sender=ArtworkComment)
# def notify_artwork_commented(sender, instance, created, **kwargs):
#     if created and instance.user != instance.artwork.artist:
#         print(f"[post_save] Artwork commented - notify artist")
#         Notification.objects.create(
#             recipient=instance.artwork.artist,
#             actor=instance.user,
#             verb='commented on your artwork',
#             target=instance.artwork.title
#         )

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from artworks.models import Artwork, ArtworkLike, ArtworkComment
from orders.models import Order
from reviews.models import Review, ReviewLike, ReviewComment

User = get_user_model()

# ====== Cache old order status and refund status before save ======
@receiver(pre_save, sender=Order)
def cache_order_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            instance._old_status = old_order.status
            instance._old_refund_status = old_order.refund_status
        except Order.DoesNotExist:
            instance._old_status = None
            instance._old_refund_status = None
    else:
        instance._old_status = None
        instance._old_refund_status = None

# ====== Notify on order status or refund status change ======
@receiver(post_save, sender=Order)
def notify_order_changes(sender, instance, created, **kwargs):
    if created:
        # When new order created, notify seller and admins
        seller = instance.artwork.artist
        buyer = instance.user
        title = instance.artwork.title
        Notification.objects.create(
            recipient=seller,
            actor=buyer,
            verb='ordered your artwork',
            target=title
        )
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                actor=buyer,
                verb='placed a new order',
                target=title
            )
        return

    buyer = instance.user
    seller = instance.artwork.artist
    admins = User.objects.filter(is_superuser=True)
    admin_user = admins.first()
    title = instance.artwork.title

    # Notify buyer on order status change (admin confirms/cancels)
    if getattr(instance, '_old_status', None) != instance.status:
        if instance.status == 'completed':  # order confirmed by admin
            Notification.objects.create(
                recipient=buyer,
                actor=admin_user,
                verb='confirmed your order',
                target=title
            )
        elif instance.status == 'cancelled':
            Notification.objects.create(
                recipient=buyer,
                actor=admin_user,
                verb='cancelled your order',
                target=title
            )

    # Notify admins or buyer on refund status change
    if getattr(instance, '_old_refund_status', None) != instance.refund_status:
        if instance.refund_status == 'requested':
            for admin in admins:
                Notification.objects.create(
                    recipient=admin,
                    actor=buyer,
                    verb='requested a refund',
                    target=title
                )
        elif instance.refund_status == 'approved':
            Notification.objects.create(
                recipient=buyer,
                actor=admin_user,
                verb='approved your refund',
                target=title
            )
        elif instance.refund_status == 'rejected':
            Notification.objects.create(
                recipient=buyer,
                actor=admin_user,
                verb='rejected your refund',
                target=title
            )


# ====== Notify admins when new artwork created ======
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

# ====== Track artwork approval change ======
@receiver(pre_save, sender=Artwork)
def track_artwork_approval_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Artwork.objects.get(pk=instance.pk)
            instance._approval_changed = (old.is_approved != instance.is_approved)
        except Artwork.DoesNotExist:
            instance._approval_changed = False
    else:
        instance._approval_changed = False

# ====== Notify artist on artwork approval change ======
@receiver(post_save, sender=Artwork)
def notify_artwork_approval_change(sender, instance, created, **kwargs):
    if not created and getattr(instance, '_approval_changed', False):
        admin_user = User.objects.filter(is_superuser=True).first()
        Notification.objects.create(
            recipient=instance.artist,
            actor=admin_user,
            verb='approved your artwork' if instance.is_approved else 'unapproved your artwork',
            target=instance.title
        )

# ====== Notify artwork owner when new review added ======
@receiver(post_save, sender=Review)
def notify_review_added(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='reviewed your artwork',
            target=instance.artwork.title
        )

# ====== Notify review author when review liked ======
@receiver(post_save, sender=ReviewLike)
def notify_review_liked(sender, instance, created, **kwargs):
    if created and instance.user != instance.review.user:
        Notification.objects.create(
            recipient=instance.review.user,
            actor=instance.user,
            verb='liked your review',
            target=instance.review.artwork.title
        )

# ====== Notify review author when review commented ======
@receiver(post_save, sender=ReviewComment)
def notify_review_commented(sender, instance, created, **kwargs):
    if created and instance.user != instance.review.user:
        Notification.objects.create(
            recipient=instance.review.user,
            actor=instance.user,
            verb='commented on your review',
            target=instance.review.artwork.title
        )

# ====== Notify artist when artwork liked ======
@receiver(post_save, sender=ArtworkLike)
def notify_artwork_liked(sender, instance, created, **kwargs):
    if created and instance.user != instance.artwork.artist:
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='liked your artwork',
            target=instance.artwork.title
        )

# ====== Notify artist when artwork commented ======
@receiver(post_save, sender=ArtworkComment)
def notify_artwork_commented(sender, instance, created, **kwargs):
    if created and instance.user != instance.artwork.artist:
        Notification.objects.create(
            recipient=instance.artwork.artist,
            actor=instance.user,
            verb='commented on your artwork',
            target=instance.artwork.title
        )
