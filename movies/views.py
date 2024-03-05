from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListlSerializer
        return self.serializer_class


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'genres']
    search_fields = ['title', 'category__name', 'actors__name']
    ordering_fields = ['year','budget']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return self.serializer_class


class MovieShotsViewSet(ModelViewSet):
    queryset = MovieShots.objects.all()
    serializer_class = MovieShotsSerializer


class RatingStarViewSet(ModelViewSet):
    queryset = RatingStar.objects.all()
    serializer_class = RatingStarSerializer


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return self.serializer_class

    