from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ActorDetailSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class ActorListlSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = 'name', 'image'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RecursiveSerializer(Serializer):                       #create nested list
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(ListSerializer):
    def to_representation(self, data):
        if hasattr(data, 'all'):
            related_reviews = data.all()  # Получаем все связанные объекты
        else:
            related_reviews = data  # Используем исходные данные, если это уже список
        # Фильтруем данные, оставляя только записи с parent=None
        filtered_data = [item for item in related_reviews if item.parent is None]        
        # Передаем отфильтрованные данные для дальнейшей сериализации
        return super().to_representation(filtered_data)


class ReviewListSerializer(ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = 'user', 'text', 'children'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class MovieListSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title', 'poster', 'category'


class MovieDetailSerializer(ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
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
        