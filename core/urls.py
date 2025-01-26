from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:userhandle>', views.profile, name='profile'),
    path('liked', views.liked, name='liked'),
    path('saved/', views.saved, name='saved'),
]
