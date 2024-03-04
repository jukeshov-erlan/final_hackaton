from rest_framework.viewsets import ModelViewSet
from .serializers import *


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


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
    serializer_class = ReviewSerializer
    