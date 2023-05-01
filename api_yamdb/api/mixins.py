from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   DestroyModelMixin)

from .permissions import IsAdminOrReadOnly


class CategoryAndGenreMixinViewSet(CreateModelMixin,
                                   ListModelMixin,
                                   DestroyModelMixin,
                                   viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
