from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username, UsernameRegexValidator


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        default_related_name = "categories"


class Genre(models.Model):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        default_related_name = "genres"


class Title(models.Model):
    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLES = (
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
    )
    username_validator = UsernameRegexValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Пользователь",
        validators=(username_validator, validate_username,),
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Почта",
    )
    first_name = models.CharField(max_length=150, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, null=True, verbose_name="Фамилия")
    bio = models.TextField(
        blank=True,
        verbose_name="Кратко о себе",
    )
    role = models.CharField(
        max_length=max([len(role) for role, name in ROLES]),
        choices=ROLES,
        default=USER,
        verbose_name="Роль",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            ),
        ]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
