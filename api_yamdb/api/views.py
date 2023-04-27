from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, views, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User
from .permissions import AdminOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TokenSerializer,
    UserEditSerializer,
    UserSerializer,
    UserSignUpSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки всех категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки всех произведений.
    """

    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки всех жанров.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticated,
        AdminOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
        serializer_class=UserEditSerializer,
    )
    def get_me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignupAPIView(views.APIView):
    """User register API."""

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    lookup_field = "username"

    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(username=request.data["username"])
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject="Код подтверждения для регистрации на yamdb",
                message=f"Код подтверждения для пользователя {user.username}:"
                f" {confirmation_code}",
                from_email="from@example.com",
                recipient_list=[f"{user.email}"],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(views.APIView):
    """Refresh token."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data["username"])
        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]
        ):
            token = RefreshToken.for_user(user).access_token
            return Response({"token": str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
