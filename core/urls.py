from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CreateUserView,
    UserProfileView,
    InterestCategoryListView,
    InterestListView,
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
    path("interests/", InterestListView.as_view(), name="interest-list"),
]
