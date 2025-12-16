from django.shortcuts import render
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        return Response(
            {
                "message": "Account created successfully",
                "user": UserSerializer(user).data,
                "access": access,
                "refresh": str(refresh), },
            status=status.HTTP_201_CREATED,
        )


# LOGIN VIEW
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

      
        return Response(
            {
                "message": "Login successful",
                "user": UserSerializer(user).data,
                "access": access,
                "refresh": str(refresh),
            
            },
            status=status.HTTP_200_OK,
        )
