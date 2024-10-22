from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserInterest, UserProfile, InterestCategory, Interest


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserInterestsTabular(admin.TabularInline):
    model = UserInterest


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (UserProfileInline, UserInterestsTabular)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(InterestCategory)
admin.site.register(Interest)
