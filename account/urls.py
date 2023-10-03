from django.urls import path
from . import views

urlpatterns = [
    path('user-registration/', views.UserRegistration, name="user-registration"),
    path('user-login/', views.UserLogin, name="user-login")
]
