
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=128,
        help_text="Password must be at least 8 characters long."
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'mobile']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_mobile(self, value):
        if value and User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.password = make_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=128,
        help_text="Password must be at least 8 characters long."
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid email or password")

        if user.block_user == '1':
            raise serializers.ValidationError("User account is blocked")

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile']