from django.urls import path
from .views import MatchingProfilesView, PublicProfileView, CommonInterestsUsersView

urlpatterns = [
    path("matching-profiles/", MatchingProfilesView.as_view(), name="matching_profiles"),
    path(
        "users/<uuid:user_id>/public-profile/",
        PublicProfileView.as_view(),
        name="public-profile",
    ),
    path(
        "users/common-interests/",
        CommonInterestsUsersView.as_view(),
        name="common-interests",
    ),
]
