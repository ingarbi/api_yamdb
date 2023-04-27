import re

from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r"^[\w.@+-]+\Z"
    flags = 0


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            ("Имя пользователя не может быть <me>."),
            params={"value": value},
        )
    return value