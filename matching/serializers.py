from datetime import date
from rest_framework import serializers
from core.models import UserProfile, UserInterest


class PublicUserInterestSerializer(serializers.ModelSerializer):
    interest_name = serializers.CharField(source="interest.name", read_only=True)
    category_name = serializers.CharField(source="interest.category.name", read_only=True)

    class Meta:  # type: ignore
        model = UserInterest
        fields = ("interest_name", "category_name")
        read_only_fields = fields


class PublicProfileSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(source="user.public_id", read_only=True)
    age = serializers.SerializerMethodField()
    interests = PublicUserInterestSerializer(
        source="user.user_interests", many=True, read_only=True
    )

    class Meta:  # type: ignore
        model = UserProfile
        fields = ("public_id", "bio", "age", "interests")
        read_only_fields = fields

    def get_age(self, obj):
        if obj.birth_date:
            today = date.today()
            return (
                today.year
                - obj.birth_date.year
                - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
            )
        return None
