from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('verify/', UserVerificationAPIView.as_view(), name='user-verification'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),

    path('lawyers/', LawyerListAPIView.as_view(), name='lawyer-list'),
    path('lawyers/<int:pk>/', LawyerRetrieveAPIView.as_view(), name='lawyer-detail'),
    path('customers/', CustomerListAPIView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerRetrieveAPIView.as_view(), name='customer-detail'),
]
