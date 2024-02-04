from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, AdminProfile, LawyerProfile, CustomerProfile
from .serializers import CustomUserSerializer, AdminProfileSerializer, LawyerProfileSerializer, CustomerProfileSerializer

class CustomUserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            user.set_password(request.data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User registered successfully',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        print(user)

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        admin_profile = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(admin_profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        admin_profile = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(admin_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        admin_profile = AdminProfile.objects.get(user=request.user)
        admin_profile.delete()
        return Response({'message': 'Admin profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class LawyerProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lawyer_profile = LawyerProfile.objects.get(user=request.user)
        serializer = LawyerProfileSerializer(lawyer_profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        lawyer_profile = LawyerProfile.objects.get(user=request.user)
        serializer = LawyerProfileSerializer(lawyer_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        lawyer_profile = LawyerProfile.objects.get(user=request.user)
        lawyer_profile.delete()
        return Response({'message': 'Lawyer profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CustomerProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        customer_profile = CustomerProfile.objects.get(user=request.user)
        serializer = CustomerProfileSerializer(customer_profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        customer_profile = CustomerProfile.objects.get(user=request.user)
        serializer = CustomerProfileSerializer(customer_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        customer_profile = CustomerProfile.objects.get(user=request.user)
        customer_profile.delete()
        return Response({'message': 'Customer profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
