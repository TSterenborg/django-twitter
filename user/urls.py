from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:userhandle>/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
]
