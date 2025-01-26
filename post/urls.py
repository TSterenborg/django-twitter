from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
]