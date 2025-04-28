from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    
    
]
