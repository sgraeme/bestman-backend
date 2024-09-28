from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # email is the username
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email"]


class InterestCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Interest Categories"


class Interest(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        InterestCategory, on_delete=models.CASCADE, related_name="interests"
    )

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name_plural = "Interests"
        unique_together = ("name", "category")


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"


class UserInterestCategoryRanking(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="interest_category_rankings"
    )
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Importance ranking from 1 (least important) to 5 (most important)",
    )

    def __str__(self):
        return (
            f"{self.user.email} - {self.category.name} (Importance: {self.importance})"
        )

    class Meta:
        unique_together = ("user", "category")


class UserInterest(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_interests"
    )
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.interest.name}"

    class Meta:
        unique_together = ("user", "interest")
