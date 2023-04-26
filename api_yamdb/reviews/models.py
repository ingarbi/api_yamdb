from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


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
    class Roles(models.TextChoices):
        USER = "Пользователь", _("user")
        MODERATOR = "Модератор", _("moderator")
        ADMIN = "Администратор", _("admin")
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Пользователь",
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Почта",
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name="Фамилия"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Кратко о себе",
    )
    role = models.CharField(
        max_length=max(len(role[0]) for role in Roles.choices),
        choices=Roles.choices,
        default=Roles.USER,
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
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    @property
    def is_user(self):
        return self.role == self.Roles.USER

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    def __str__(self):
        return self.username
