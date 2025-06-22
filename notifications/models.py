# from django.db import models
# from django.conf import settings
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Notification(models.Model):
#     recipient = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='notifications'
#     )
#     actor = models.ForeignKey(
#         User,
#         null=True,  # allow null
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='notifications_sent'
#     )

#     verb = models.CharField(max_length=255)
#     target = models.CharField(max_length=255, null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     unread = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.actor} {self.verb} {self.target or ''} → {self.recipient}"

# from django.db import models
# from django.conf import settings

# class Notification(models.Model):
#     recipient = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='notifications'
#     )
#     actor = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='notifications_sent'
#     )
#     verb = models.CharField(max_length=255)
#     target = models.CharField(max_length=255, null=True, blank=True)
#     url = models.URLField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     unread = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.actor} {self.verb} {self.target or ''} → {self.recipient}"

from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications_sent'
    )
    verb = models.CharField(max_length=255)
    target = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target or ''} → {self.recipient}"

    def get_absolute_url(self):
        if self.url:
            return self.url
        return '#'
