from rest_framework import serializers
from .models import (
    CustomUser,
    UserProfile,
    InterestCategory,
    Interest,
    UserInterestCategoryImportance,
    UserInterest,
)


class UserSerializer(serializers.ModelSerializer[CustomUser]):
    class Meta:  # type: ignore
        model = CustomUser
        fields = ("id", "email")
        read_only_fields = ("id", "email")


class UserCreateSerializer(serializers.ModelSerializer[CustomUser]):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:  # type: ignore
        model = CustomUser
        fields = ("email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer[UserProfile]):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:  # type: ignore
        model = UserProfile
        fields = ("email", "bio", "birth_date")
        read_only_fields = ("email", "birth_date")


class InterestCategorySerializer(serializers.ModelSerializer[InterestCategory]):
    class Meta:  # type: ignore
        model = InterestCategory
        fields = ("id", "name")


class InterestSerializer(serializers.ModelSerializer[Interest]):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:  # type: ignore
        model = Interest
        fields = ("id", "name", "category", "category_name")


class UserInterestSerializer(serializers.ModelSerializer[UserInterest]):
    interest_name = serializers.CharField(source="interest.name", read_only=True)
    category_name = serializers.CharField(
        source="interest.category.name", read_only=True
    )

    class Meta:  # type: ignore
        model = UserInterest
        fields = ("id", "user", "interest", "interest_name", "category_name")
        read_only_fields = ("user",)


class UserInterestCategoryImportanceSerializer(
    serializers.ModelSerializer[UserInterestCategoryImportance]
):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:  # type: ignore
        model = UserInterestCategoryImportance
        fields = ("id", "user", "category", "category_name", "importance")
        read_only_fields = ("user",)


class UserInterestsBulkUpdateSerializer(serializers.Serializer):
    interest_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )

    def validate_interest_ids(self, value):
        # Check if all provided interest IDs exist
        existing_ids = set(
            Interest.objects.filter(id__in=value).values_list("id", flat=True)
        )
        invalid_ids = set(value) - existing_ids
        if invalid_ids:
            raise serializers.ValidationError(
                f"Invalid interest IDs: {', '.join(map(str, invalid_ids))}"
            )
        return value
