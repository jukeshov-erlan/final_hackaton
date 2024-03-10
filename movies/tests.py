from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Movie

class MovieViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.admin_user = User.objects.create_superuser(username='admin_user', email='admin@example.com', password='admin_password')
        self.movie = Movie.objects.create(title='Test Movie', year=2022, budget=1000000)

    def test_get_movie_list(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie_detail(self):
        response = self.client.get(f'/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_movie_unauthorized(self):
        data = {'title': 'New Movie', 'year': 2023, 'budget': 1500000}
        response = self.client.post('/movies/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_movie_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New Movie', 'year': 2023, 'budget': 1500000}
        response = self.client.post('/movies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_movie_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'New Movie', 'year': 2023, 'budget': 1500000}
        response = self.client.post('/movies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Similarly, you can add more tests for update, partial_update, and destroy actions

    def test_update_movie_unauthorized(self):
        data = {'title': 'Updated Movie'}
        response = self.client.put(f'/movies/{self.movie.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_movie_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Movie'}
        response = self.client.put(f'/movies/{self.movie.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_movie_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Updated Movie'}
        response = self.client.put(f'/movies/{self.movie.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add tests for other actions like partial_update and destroy as needed

    # Add tests for other viewsets (ActorViewSet, GenreViewSet, etc.) similarly

