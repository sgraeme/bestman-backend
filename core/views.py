from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from core.models import UserProfile
from .serializers import UserCreateSerializer, UserProfileSerializer

CustomUser = get_user_model()


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return the UserProfile for the currently authenticated user.
        """
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        """
        Returns the UserProfile object for the current user.
        If it doesn't exist, it creates a new one.
        """
        queryset = self.get_queryset()
        obj, created = queryset.get_or_create(user=self.request.user)
        if created:
            # TODO: Make this proper logging
            print("A new profile was created.")
        return obj
