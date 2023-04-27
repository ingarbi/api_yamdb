from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings
from reviews.validators import UsernameValidatorMixin

from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer, UsernameValidatorMixin):
    email = serializers.EmailField(
        max_length=settings.DEFAULT_EMAIL_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class RegisterDataSerializer(
    serializers.ModelSerializer,
    UsernameValidatorMixin
):
    email = serializers.EmailField(
        max_length=settings.DEFAULT_EMAIL_LENGTH,
        required=True,
    )

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer, UsernameValidatorMixin):
    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=settings.DEFAULT_FIELD_LENGTH,
        required=True,
    )
