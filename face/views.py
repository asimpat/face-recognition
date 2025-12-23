from django.shortcuts import render
from .serializers import UserSerializer, LoginSerializer, FaceSerializer, FaceVerifySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Face



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


class FaceEnrollView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # link face to logged-in user
        return Response(
            {"message": "Face enrolled successfully", "face": serializer.data},
            status=status.HTTP_201_CREATED
        )


class FaceVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FaceVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get submitted image
        submitted_image = serializer.validated_data['image']

        # Get the user's enrolled face
        try:
            enrolled_face = request.user.face
        except Face.DoesNotExist:
            return Response(
                {"error": "No face enrolled for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )


        # TODO: Face recognition logic here
        # For now, we'll simulate a match
        match = True
        confidence = 0.95  

        if match:
            return Response(
                {
                    "message": "Face verified successfully",
                    "confidence": confidence
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Face verification failed", "confidence": confidence},
                status=status.HTTP_401_UNAUTHORIZED
            )