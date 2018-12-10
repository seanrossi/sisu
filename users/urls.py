# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.HomePageView.as_view(), name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]