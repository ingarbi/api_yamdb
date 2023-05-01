from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import UsernameValidatorMixin, validate_year


class User(AbstractUser, UsernameValidatorMixin):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = (
        (ADMIN, "Administrator"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True,
        max_length=settings.DEFAULT_EMAIL_LENGTH,
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=settings.DEFAULT_FIELD_LENGTH,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(verbose_name="О себе", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == self.USER


class Category(models.Model):
    name = models.CharField(
        max_length=settings.LIMIT_CHAT,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.MAX_SLUG_LENGTH,
        verbose_name="Слаг",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("slug",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=settings.LIMIT_CHAT,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.MAX_SLUG_LENGTH,
        verbose_name="Слаг",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("slug",)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=settings.LIMIT_CHAT,
        verbose_name="Название произведения",
    )
    year = models.PositiveSmallIntegerField(
        db_index=True,
        validators=[
            validate_year,
        ],
        verbose_name="Год выпуска",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    genre = models.ManyToManyField(
        Genre, blank=True, through="GenreTitle", verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("name",)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Название произведения",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Название жанра",
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения",
    )
    text = models.TextField(verbose_name="Текст для ревью")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.MIN_LIMIT_VALUE),
            MaxValueValidator(settings.MAX_LIMIT_VALUE),
        ],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review"
            )
        ]
        ordering = ("pub_date",)

    def __str__(self):
        return self.text[: settings.CHARS_LIMIT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Ревью",
    )
    text = models.TextField(
        verbose_name="Текст для комментария",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("pub_date",)

    def __str__(self):
        return self.text[: settings.CHARS_LIMIT]
