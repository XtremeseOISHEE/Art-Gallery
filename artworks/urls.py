from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('artworks/', views.artwork_list, name='artwork_list'), 
    path('create/', views.artwork_create, name='artwork_create'),
    path('<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('<int:pk>/edit/', views.artwork_edit, name='artwork_edit'),
    path('<int:pk>/delete/', views.artwork_delete, name='artwork_delete'),
    path('<int:pk>/approve/', views.artwork_approve, name='artwork_approve'),
    path('artworks/search/', views.artwork_search, name='artwork_search'),
    path('my-arts/', views.my_artworks, name='my_artworks'),
    path('admin/pending-artworks/', views.pending_artworks, name='pending_artworks'),
    path('admin/approve-artwork/<int:pk>/', views.artwork_approve, name='artwork_approve'),
]
