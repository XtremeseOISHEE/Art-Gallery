# from django.urls import path
# from .views import my_notifications

# urlpatterns = [
#      path('', my_notifications, name='my_notifications'),
# #  ]

# from django.urls import path
# from .views import my_notifications

# urlpatterns = [
#     path('', my_notifications, name='my_notifications'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.my_notifications, name='my_notifications'),
    path('notifications/<int:pk>/redirect/', views.notification_redirect, name='notification_redirect'),
]
