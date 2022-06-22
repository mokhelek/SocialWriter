"""Defines URL patterns for users"""
from django.urls import path, include
from .import views


app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),  #the login and logout are in here
    
    path('register/', views.register, name='register'),
    #path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logoutpage'),
    
]