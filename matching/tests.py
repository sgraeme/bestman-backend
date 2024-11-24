from unittest.mock import Mock
from django.test import TestCase
from rest_framework.request import Request as DRFRequest
from rest_framework.test import APIClient
from core.models import CustomUser, Interest, InterestCategory, UserInterest, UserProfile
from .views import CommonInterestsUsersView


class CommonInterestsUsersViewTests(TestCase):
    # Constants for categories
    CATEGORY_SPORTS = "Sports"
    CATEGORY_MUSIC = "Music"

    # Constants for interests
    INTEREST_FOOTBALL = "Football"
    INTEREST_BASKETBALL = "Basketball"
    INTEREST_ROCK = "Rock"
    INTEREST_JAZZ = "Jazz"

    # Constants for user emails
    USER1_EMAIL = "user1@test.com"
    USER2_EMAIL = "user2@test.com"
    USER3_EMAIL = "user3@test.com"
    USER4_EMAIL = "user4@test.com"

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.setup_categories_and_interests()
        cls.setup_users()
        cls.setup_user_interests()

    @classmethod
    def setup_categories_and_interests(cls):
        cls.categories = {
            cls.CATEGORY_SPORTS: InterestCategory.objects.create(name=cls.CATEGORY_SPORTS),
            cls.CATEGORY_MUSIC: InterestCategory.objects.create(name=cls.CATEGORY_MUSIC),
        }
        cls.interests = {
            cls.INTEREST_FOOTBALL: Interest.objects.create(
                name=cls.INTEREST_FOOTBALL, category=cls.categories[cls.CATEGORY_SPORTS]
            ),
            cls.INTEREST_BASKETBALL: Interest.objects.create(
                name=cls.INTEREST_BASKETBALL, category=cls.categories[cls.CATEGORY_SPORTS]
            ),
            cls.INTEREST_ROCK: Interest.objects.create(
                name=cls.INTEREST_ROCK, category=cls.categories[cls.CATEGORY_MUSIC]
            ),
            cls.INTEREST_JAZZ: Interest.objects.create(
                name=cls.INTEREST_JAZZ, category=cls.categories[cls.CATEGORY_MUSIC]
            ),
        }

    @classmethod
    def setup_users(cls):
        cls.users = {
            "user1": cls.create_user(cls.USER1_EMAIL),
            "user2": cls.create_user(cls.USER2_EMAIL),
            "user3": cls.create_user(cls.USER3_EMAIL),
            "user4": cls.create_user(cls.USER4_EMAIL),
        }

    @classmethod
    def create_user(cls, email):
        user = CustomUser.objects.create_user(email=email, password="testpass123")
        UserProfile.objects.create(user=user)
        return user

    @classmethod
    def setup_user_interests(cls):
        user_interests = {
            "user1": [cls.INTEREST_FOOTBALL, cls.INTEREST_BASKETBALL],
            "user2": [cls.INTEREST_FOOTBALL, cls.INTEREST_BASKETBALL, cls.INTEREST_ROCK],
            "user3": [cls.INTEREST_FOOTBALL, cls.INTEREST_ROCK],
            "user4": [cls.INTEREST_ROCK, cls.INTEREST_JAZZ],
        }
        for user, interests in user_interests.items():
            for interest in interests:
                UserInterest.objects.create(user=cls.users[user], interest=cls.interests[interest])

    def setUp(self):
        self.view = CommonInterestsUsersView()
        self.mock_request = Mock(spec=DRFRequest)
        self.mock_request.user = self.users["user1"]
        self.view.request = self.mock_request

    def get_queryset_results(self):
        return list(self.view.get_queryset())

    def test_common_interests_query(self):
        """Test the query returns users ordered by shared interests count"""
        users = self.get_queryset_results()
        self.assertEqual(len(users), 2)  # Only users with shared interests
        self.assertEqual(users[0].user.email, self.USER2_EMAIL)  # Most shared interests
        self.assertEqual(users[1].user.email, self.USER3_EMAIL)  # Second most shared

    def test_excludes_users_without_shared_interests(self):
        """Test that users without shared interests are excluded from results"""
        users = self.get_queryset_results()
        user4_present = any(profile.user.email == self.USER4_EMAIL for profile in users)
        self.assertFalse(user4_present)

    def test_excludes_self(self):
        """Test that the user is not included in their own results"""
        users = self.get_queryset_results()
        user1_emails = [
            profile.user.email for profile in users if profile.user.email == self.USER1_EMAIL
        ]
        self.assertEqual(len(user1_emails), 0)
