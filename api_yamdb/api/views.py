from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filiters import TitleFilter
from .permissions import IsAdmin
from .serializers import (
    CategorySerializer,
    # CommentSerializer,
    GenreSerializer,
    RegisterDataSerializer,
    # ReviewSerializer,
    TitlePostSerializer,
    # TitleReadSerializer,
    TitleSerializer,
    # TitleWriteSerializer,
    TokenSerializer,
    UserEditSerializer,
    UserSerializer,
)
from .utils import confirmation_mail


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки всех категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки всех жанров.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)
    filterset_class = TitleFilter
    filterset_fields = ("name",)
    ordering = ("name",)

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return TitlePostSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            title=title,
            # author=self.request.user,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()


@api_view(["POST"])
def register(request):
    serializer = RegisterDataSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get("username"), email=request.data.get("email")
    ).exists():
        user_in_base = User.objects.get(
            username=request.data.get("username"),
            email=request.data.get("email"),
        )
        confirmation_mail(user_in_base)
        return Response(request.data, status=status.HTTP_200_OK)
    try:
        serializer.is_valid(raise_exception=True)
        user, create = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise ValidationError("Неверное имя пользователя или email")
    confirmation_mail(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data.get("username"))

    if default_token_generator.check_token(
        user, serializer.validated_data.get("confirmation_code")
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
        url_path="me",
    )
    def get_me(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
