from rest_framework import viewsets, mixins, filters, permissions, serializers
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from . filters import TitleFilter
from .permissions import IsAuthorOrSuperUser, IsSuperUser
from .models import Title, Category, Genre, Review
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleGetSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        self.titles = Title.objects.all()
        for title in self.titles:
            reviews_nb = title.reviews.all().count()
            if reviews_nb > 0:
                return Title.objects.annotate(
                    rating=models.Sum(
                        models.F('reviews__score')) / models.Count('reviews')
                )
            return Title.objects.annotate(
                rating=models.Sum(models.F('reviews__score'))
            )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        else:
            return TitleSerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthorOrSuperUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        is_unique = Review.objects.filter(
            author=self.request.user, title=title
        ).exists()
        if is_unique:
            raise serializers.ValidationError(
                "Вы уже писали отзыв к этому произведению."
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthorOrSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
