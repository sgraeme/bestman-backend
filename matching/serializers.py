from datetime import date
from rest_framework import serializers
from core.serializers import UserInterestSerializer
from core.models import UserProfile


class PublicProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    interests = UserInterestSerializer(source="user.user_interests", many=True, read_only=True)

    class Meta:  # type: ignore
        model = UserProfile
        fields = ("bio", "age", "interests")
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
