from django.shortcuts import get_object_or_404
from rest_framework import generics
from core.models import UserProfile
from .serializers import PublicProfileSerializer


class MatchingProfilesView(generics.ListAPIView):
    serializer_class = PublicProfileSerializer
    queryset = UserProfile.objects.all()


class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = PublicProfileSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(
            UserProfile.objects.select_related("user").prefetch_related(
                "user__user_interests__interest__category"
            ),
            user__id=user_id,
        )
