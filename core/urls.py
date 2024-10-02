from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CreateUserView,
    UserProfileView,
    InterestCategoryListView,
    InterestListView,
    UserInterestView,
    UserInterestCategoryImportanceView,
    UserInterestsBulkUpdateView,
)


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "interest-categories/",
        InterestCategoryListView.as_view(),
        name="interest-category-list",
    ),
    path("interests/", InterestListView.as_view(), name="interest_list"),
    path("user-interests/", UserInterestView.as_view(), name="user_interests"),
    path(
        "user-interest-category-importances/",
        UserInterestCategoryImportanceView.as_view(),
        name="user_interest_category_importances",
    ),
    path(
        "user-interests-bulk-update/",
        UserInterestsBulkUpdateView.as_view(),
        name="user_interests_bulk_update",
    ),
]
