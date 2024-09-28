from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from core.models import (
    UserProfile,
    InterestCategory,
    Interest,
    UserInterest,
    UserInterestCategoryImportance,
)
from .serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    InterestCategorySerializer,
    InterestSerializer,
    UserInterestSerializer,
    UserInterestCategoryImportanceSerializer,
)

CustomUser = get_user_model()


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # type: ignore
        """
        This view should return the UserProfile for the currently authenticated user.
        """
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self) -> UserProfile:
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


class InterestCategoryListView(generics.ListAPIView):
    queryset = InterestCategory.objects.all()
    serializer_class = InterestCategorySerializer
    permission_classes = (permissions.AllowAny,)


class InterestListView(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = (permissions.AllowAny,)


class UserInterestView(generics.ListCreateAPIView):
    serializer_class = UserInterestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # type: ignore
        return UserInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer: UserInterestSerializer) -> None:
        serializer.save(user=self.request.user)


class UserInterestCategoryRankingView(generics.ListCreateAPIView):
    serializer_class = UserInterestCategoryImportanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # type: ignore
        return UserInterestCategoryImportance.objects.filter(user=self.request.user)

    def perform_create(
        self, serializer: UserInterestCategoryImportanceSerializer
    ) -> None:
        serializer.save(user=self.request.user)
