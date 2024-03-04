from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('actors', ActorViewSet)
router.register('genres', GenreViewSet)
router.register('movies', MovieViewSet)
router.register('movieshots', MovieShotsViewSet)
router.register('ratingstars', RatingStarViewSet)
router.register('ratings', RatingViewSet)
router.register('reviews', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
]


