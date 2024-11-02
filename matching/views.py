from typing import Union
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from core.models import CustomUser, Interest, UserProfile
from .serializers import PublicProfileSerializer


class MatchingProfilesView(generics.ListAPIView):
    serializer_class = PublicProfileSerializer
    queryset = UserProfile.objects.all()


class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = PublicProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(
            UserProfile.objects.select_related("user").prefetch_related(
                "user__user_interests__interest__category"
            ),
            user__public_id=user_id,
        )


class CommonInterestsUsersView(generics.ListAPIView):
    serializer_class = PublicProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
        user: Union[CustomUser, AnonymousUser] = self.request.user
        if isinstance(user, AnonymousUser):
            return UserProfile.objects.none()

        return (
            UserProfile.objects.exclude(user_id=user.id)
            .filter(
                user__user_interests__interest__in=Interest.objects.filter(userinterest__user=user)
            )
            .annotate(
                shared_interests_count=Count(
                    "user__user_interests",
                    filter=Q(
                        user__user_interests__interest__in=Interest.objects.filter(
                            userinterest__user=user
                        )
                    ),
                )
            )
            # email as secondary ordering for consistency but can be anything
            .order_by("-shared_interests_count", "user__email")
            .distinct()
        )
