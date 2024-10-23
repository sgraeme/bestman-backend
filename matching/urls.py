from django.urls import path
from .views import MatchingProfilesView, PublicProfileView

urlpatterns = [
    path("matching-profiles/", MatchingProfilesView.as_view(), name="matching_profiles"),
    path(
        "users/<int:user_id>/public-profile/",
        PublicProfileView.as_view(),
        name="public-profile",
    ),
]
