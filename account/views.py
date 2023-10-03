from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from .serializer import UserSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
@api_view(['POST'])
def UserRegistration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse({"message": "Account created successfully!"})
    return JsonResponse({"message": "An error occured"}, HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def UserLogin(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)    
    token = str(refresh.access_token)

    return JsonResponse({'token': token}, status=status.HTTP_200_OK)
