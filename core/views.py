from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction

from core.models import (
    UserProfile,
    InterestCategory,
    Interest,
    UserInterest,
    UserInterestCategoryRanking,
)
from .serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    InterestCategorySerializer,
    InterestSerializer,
    UserInterestSerializer,
    UserInterestCategoryRankingSerializer,
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

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        interest_ids = request.data.get("interest_ids", [])
        if not isinstance(interest_ids, list):
            return Response(
                {"error": "interest_ids must be a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_interests = []
        for interest_id in interest_ids:
            interest = Interest.objects.filter(id=interest_id).first()
            if interest:
                user_interest, created = UserInterest.objects.get_or_create(
                    user=request.user, interest=interest
                )
                if created:
                    created_interests.append(self.serializer_class(user_interest).data)

        return Response({"created": created_interests}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        interest_ids = request.data.get("interest_ids", [])
        if not isinstance(interest_ids, list):
            return Response(
                {"error": "interest_ids must be a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count = UserInterest.objects.filter(
            user=request.user, interest__id__in=interest_ids
        ).delete()[0]

        return Response(
            {"message": f"Successfully deleted {deleted_count} UserInterest(s)"},
            status=status.HTTP_200_OK,
        )


class UserInterestCategoryRankingView(generics.ListCreateAPIView):
    serializer_class = UserInterestCategoryRankingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # type: ignore
        return UserInterestCategoryRanking.objects.filter(user=self.request.user)

    def perform_create(self, serializer: UserInterestCategoryRankingSerializer) -> None:
        serializer.save(user=self.request.user)

    def perform_update(self, serializer: UserInterestCategoryRankingSerializer) -> None:
        serializer.save()

    def post(self, request, *args, **kwargs):
        rankings_data = request.data
        if not isinstance(rankings_data, list):
            rankings_data = [rankings_data]

        created_rankings = []
        updated_rankings = []

        for ranking_data in rankings_data:
            ranking_id = ranking_data.get("id")
            if ranking_id:
                # Update existing ranking
                try:
                    user_ranking = UserInterestCategoryRanking.objects.get(
                        id=ranking_id, user=request.user
                    )
                    serializer = self.get_serializer(
                        user_ranking, data=ranking_data, partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    updated_rankings.append(serializer.data)
                except UserInterestCategoryRanking.DoesNotExist:
                    return Response(
                        {
                            "error": f"UserInterestCategoryRanking with id {ranking_id} does not exist"
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                # Create new ranking
                serializer = self.get_serializer(data=ranking_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                created_rankings.append(serializer.data)

        return Response(
            {"created": created_rankings, "updated": updated_rankings},
            status=status.HTTP_201_CREATED,
        )
