from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'user_type', 'email_verified', 'profile_image', 'bio', 'category', 'experience', 'working_in', 'rate', 'description')
        extra_kwargs = {
            'email': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('email_verified', None)
        validated_data.pop('rate', None)
        return super().update(instance, validated_data)
