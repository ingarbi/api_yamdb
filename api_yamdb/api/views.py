from rest_framework import viewsets

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer)


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
