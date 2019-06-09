"""Defines url patterns for users aplication"""

from django.urls import path, include
from django.contrib.auth import views as auth_views

##from django.contrib.auth.forms import UserCreationForm
##from django.views.generic import FormView
##from .views import register_view, activate
from . import views

app_name = 'users'
urlpatterns = [
    # Login page.
    path('login/',
    	auth_views.LoginView.as_view(template_name='users/login.html'),
    	name='login'),

    #Logout page.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #Register page.
    path('register/', views.register, name='register'),
    
]
