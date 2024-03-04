from rest_framework.serializers import ModelSerializer
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'



class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'



class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieShotsSerializer(ModelSerializer):
    class Meta:
        model = MovieShots
        fields = '__all__'



class RatingStarSerializer(ModelSerializer):
    class Meta:
        model = RatingStar
        fields = '__all__'



class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'



class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'