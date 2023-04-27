from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from reviews.validators import validate_username as val_user

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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name", "last_name", "bio", "role")
        model = User
        read_only_fields = ("role",)


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.RegexField(
        max_length=150, regex=r"^[\w.@+-]+\Z", required=True
    )

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        username = value.get("username")
        email = value.get("email")
        if username.lower() == "me":
            raise serializers.ValidationError("Нельзя использовать 'me' ")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "Другой пользователь с таким username уже существует."
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Другой пользователь с таким email уже существует."
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        return val_user(value)
