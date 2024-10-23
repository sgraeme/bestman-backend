from typing import Any, Dict
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch

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
    UserInterestsBulkUpdateSerializer,
)

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

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("interest", queryset=Interest.objects.select_related("category"))
        )

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        validated_data: Dict[str, Any] = getattr(serializer, "validated_data", {})
        interest = validated_data.get("interest")
        if interest:
            user_interest, _ = UserInterest.objects.get_or_create(user=user, interest=interest)
            serializer.instance = user_interest


class UserInterestCategoryImportanceView(
    generics.ListCreateAPIView[UserInterestCategoryImportance]
):
    serializer_class = UserInterestCategoryImportanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UserInterestCategoryImportance.objects.filter(user=self.request.user)

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        validated_data: Dict[str, Any] = getattr(serializer, "validated_data", {})
        category = validated_data.get("category")
        importance = validated_data.get("importance")
        if category is not None and importance is not None:
            user_category_importance, _ = UserInterestCategoryImportance.objects.update_or_create(
                user=user, category=category, defaults={"importance": importance}
            )
            serializer.instance = user_category_importance


class UserInterestsBulkUpdateView(generics.GenericAPIView):
    serializer_class = UserInterestsBulkUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_interest_ids: set[int] = set(serializer.validated_data["interest_ids"])

        # Remove existing UserInterests not in the new set
        UserInterest.objects.filter(user=user).exclude(interest__id__in=new_interest_ids).delete()

        # Add new UserInterests
        existing_interest_ids: set[int] = set(
            UserInterest.objects.filter(user=user).values_list("interest__id", flat=True)
        )
        interests_to_add = new_interest_ids - existing_interest_ids

        new_user_interests = [
            UserInterest(user=user, interest_id=interest_id) for interest_id in interests_to_add
        ]
        UserInterest.objects.bulk_create(new_user_interests)

        # Fetch updated UserInterests
        updated_user_interests = UserInterest.objects.filter(user=user).select_related(
            "interest__category"
        )

        # Serialize the result
        result_serializer = UserInterestSerializer(updated_user_interests, many=True)

        return Response(result_serializer.data, status=status.HTTP_200_OK)
