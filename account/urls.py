from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *

urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomUserLoginView.as_view(), name='user-login'),
    path('admin-profile/', AdminProfileDetailView.as_view(), name='admin-profile-detail'),
    path('lawyer-profile/', LawyerProfileDetailView.as_view(), name='lawyer-profile-detail'),
    path('customer-profile/', CustomerProfileDetailView.as_view(), name='customer-profile-detail'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
