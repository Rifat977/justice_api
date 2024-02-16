from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from .permission import *
from rest_framework import generics

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                otp = EmailVerificationOTP.generate_otp()
                EmailVerificationOTP.objects.create(user=user, otp=otp)
                # You can send OTP to user's email here
                return Response({'detail': 'User registered successfully. Please verify your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            otp_obj = EmailVerificationOTP.objects.get(user__email=email, otp=otp)
        except EmailVerificationOTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = otp_obj.user
        user.email_verified = True
        user.save()
        otp_obj.delete()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        new_user_type = request.data.get('user_type')
        
        current_user_type = user.user_type
        
        if new_user_type == 'admin':
            return Response({'error': 'User cannot be changed to admin'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_user_type in ['customer', 'lawyer'] and new_user_type != current_user_type:
            if current_user_type != 'admin':
                user.user_type = new_user_type
                user.save()
                serializer = CustomUserSerializer(user)
                return Response(serializer.data)
            else:
                return Response({'error': 'Admin cannot change user type'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            if user.email_verified:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email not verified'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LawyerListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_type='lawyer')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class LawyerRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type='lawyer')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class CustomerListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_type='customer')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class CustomerRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type='customer')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

