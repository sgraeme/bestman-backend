from rest_framework import serializers
from .models import (
    CustomUser,
    UserProfile,
    InterestCategory,
    Interest,
    UserInterestCategoryImportance,
    UserInterest,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email")
        read_only_fields = ("id", "email")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = ("email", "bio", "birth_date")
        read_only_fields = ("email", "birth_date")


class InterestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestCategory
        fields = ("id", "name")


class InterestSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Interest
        fields = ("id", "name", "category", "category_name")


class UserInterestSerializer(serializers.ModelSerializer):
    interest_name = serializers.CharField(source="interest.name", read_only=True)
    category_name = serializers.CharField(
        source="interest.category.name", read_only=True
    )

    class Meta:
        model = UserInterest
        fields = ("id", "user", "interest", "interest_name", "category_name")
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = validated_data["user"]
        interest = validated_data["interest"]
        user_interest, _ = UserInterest.objects.get_or_create(
            user=user, interest=interest
        )
        return user_interest


class UserInterestCategoryImportanceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = UserInterestCategoryImportance
        fields = ("id", "user", "category", "category_name", "importance")
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = validated_data["user"]
        category = validated_data["category"]
        importance = validated_data["importance"]
        user_category_importance, _ = (
            UserInterestCategoryImportance.objects.get_or_create(
                user=user, category=category, importance=importance
            )
        )
        return user_category_importance
