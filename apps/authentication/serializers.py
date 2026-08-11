from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "phone_number",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        return value


    
    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data.get(
                "phone_number",
                ""
            )
        )

        return user
    

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
        ]
        read_only_fields = [
            "id",
            "email",
        ]

class TokenRefreshSerializer(serializers.Serializer):
    
    refresh = serializers.CharField()

    def validate(self, attrs):

        refresh_token = attrs.get("refresh")

        if not refresh_token:
            raise serializers.ValidationError(
                "Refresh token is required."
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            raise serializers.ValidationError(
                "Invalid refresh token."
            )

        return {
            "access": access_token,
        }