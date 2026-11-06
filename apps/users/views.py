from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from .serializers import RegisterSerializer, GetUserSerializer, UserProfileSerializer


class RegisterView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

class GetUsers(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = GetUserSerializer

class RegisterUserProfileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    def perform_create(self, serializer):
        print(self.request.user)
        # This will now successfully pass the user ID to the database row
        serializer.save(user=self.request.user)

class GetUserProfile(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            raise NotFound(
                "User profile not found. Please create your profile first."
            )


