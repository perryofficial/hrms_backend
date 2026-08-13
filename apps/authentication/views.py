from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    TokenRefreshSerializer,
    UserSerializer,
    LogoutSerializer,
    )


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully.",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            return Response(
                {
                    "message": "Login successful",
                    "access": serializer.validated_data["access"],
                    "refresh": serializer.validated_data["refresh"],
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class TokenRefreshView(APIView):
    
    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})

        if serializer.is_valid():
            return Response(
                {
                    "access": serializer.validated_data["access"],
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )



class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )