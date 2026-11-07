from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
import logging

logger = logging.getLogger(__name__)

from .serializers import RegisterSerializer, GetUserSerializer, UserProfileSerializer, UpdateUserSerializer, UpdateUserProfileSerializer


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class GetUsers(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = GetUserSerializer

class UpdateUser(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    def get_object(self):
        return self.request.user

class DeleteUser(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            return Response(
                {"message": "User has been deleted successfully."},
                status=status.HTTP_200_OK
            )

        except Exception:
            logger.exception("Error occurred while deleting user")

            raise APIException(
                "Something went wrong while deleting the user."
            )

class RegisterUserProfileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    def perform_create(self, serializer):
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

class UpdateUserProfile(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserProfileSerializer
    def get_queryset(self):
      return UserProfile.objects.filter(user=self.request.user) #only current users user profile will get not others