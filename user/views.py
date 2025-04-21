from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import User
from user.serializers import SignupSerializer, LoginSerializer, UserSerializer, ProfileSerializer
from rest_framework import status, viewsets


class SignupViewSet(ViewSet):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User Registered Successfully",
            "user": self.serializer_class(user).data,
            "role": user.role,
        },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User Logged In Successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({
            "message": "User deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save()
