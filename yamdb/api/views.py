from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets, pagination,
                            permissions, mixins, filters)

from . import serializers
from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrAdminOrModeratorOrReadOnly
)
from .. import models


class ListCreateDeleteViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    """Displaying a list, creating and deleting an object."""
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    """Output categories."""
    queryset = models.Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.CategorySerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(ListCreateDeleteViewSet):
    """Output genres."""
    queryset = models.Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.GenreSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Output creative works."""
    queryset = (models.Title.objects.select_related('category')
                .prefetch_related('genre').annotate(
        rating=Avg('review__score')).order_by('-year'))
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return serializers.TitleCreateSerializer
        return serializers.TitleDefaultSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD API for Review."""
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminOrModeratorOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs['title_id'])
        return title.review.select_related('author').all()

    def perform_create(self, serializer):
        title = get_object_or_404(models.Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD API for Comments."""
    serializer_class = serializers.CommentSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminOrModeratorOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            models.Review, title=self.kwargs['title_id'],
            id=self.kwargs['review_id'])
        return review.comment.select_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            models.Review, title=self.kwargs['title_id'],
            id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
