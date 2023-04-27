from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from rest_framework import serializers


class UsernameValidatorMixin:
    username = models.CharField(
        max_length=settings.DEFAULT_FIELD_LENGTH,
        verbose_name="Имя пользователя",
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Имя пользователя содержит недопустимый символ",
            )
        ],
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Имя пользователя 'me'- не доступно"
            )
        return value
