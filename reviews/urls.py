# from django.urls import path
# from . import views
# from .views import create_review, like_review, add_comment, delete_review
# urlpatterns = [
#     path('artwork/<int:artwork_id>/review/', views.create_review, name='create_review'),
#     path('review/<int:review_id>/like/', views.like_review, name='like_review'),
#     path('review/<int:review_id>/comment/', views.add_comment, name='add_comment'),
#     path('review/<int:review_id>/delete/', delete_review, name='delete_review')
#     path('review/edit/<int:pk>/', views.edit_review, name='edit_review'),
#     path('comment/edit/<int:pk>/', views.edit_comment, name='edit_comment'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('artwork/<int:artwork_id>/review/', views.create_review, name='create_review'),
    path('review/<int:review_id>/like/', views.like_review, name='like_review'),
    path('review/<int:review_id>/comment/', views.add_comment, name='add_comment'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
