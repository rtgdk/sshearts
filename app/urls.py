from django.urls import path
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('deauthorize/', views.user_deauthorize, name= 'deauthorize'),
]
