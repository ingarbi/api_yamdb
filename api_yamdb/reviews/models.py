from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .utilites import current_year
from .validators import UsernameValidatorMixin


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

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField("Название произведения", max_length=settings.LIMIT_CHAT)
    year = models.PositiveSmallIntegerField(
        "Год выпуска",
        db_index=True,
        validators=[
            MinValueValidator(
                limit_value=settings.MIN_LIMIT_VALUE,
                message="Год не может быть меньше или равен нулю",
            ),
            MaxValueValidator(
                limit_value=current_year, message="Год не может быть больше текущего"
            ),
        ],
    )
    description = models.TextField("Описание", blank=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through="GenreTitle",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("name",)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        ordering = ("pub_date",)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("pub_date",)

    def __str__(self):
        return self.text


