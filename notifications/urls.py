# from django.urls import path
# from .views import my_notifications

# urlpatterns = [
#      path('', my_notifications, name='my_notifications'),
#  ]

from django.urls import path
from .views import my_notifications

urlpatterns = [
    path('', my_notifications, name='my_notifications'),
]
