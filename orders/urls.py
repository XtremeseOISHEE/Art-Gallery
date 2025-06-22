from django.urls import path
from . import views
from .views import finalize_payment, cart_order_confirm

urlpatterns = [
    path('create/<int:artwork_id>/', views.create_order, name='create_order'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    
    path('orders/', views.order_list, name='order_list'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:artwork_id>/', views.add_to_cart, name='add_to_cart'),
    path('proceed-to-payment/', views.proceed_to_payment, name='proceed_to_payment'),
    path('order/<int:order_id>/confirm/', views.order_confirm, name='order_confirm'),
    
    path('cart/finalize/', finalize_payment, name='finalize_payment'),
    path('cart/confirm/', cart_order_confirm, name='cart_order_confirm'),
]
