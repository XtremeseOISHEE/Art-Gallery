from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:artwork_id>/', views.create_order, name='create_order'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
