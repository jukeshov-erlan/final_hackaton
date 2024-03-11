from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from .views import RegisterView, ActivateView, LogoutAPIView, ChangePasswordView, ForgotPasswordCompleteView, \
    ForgotPasswordView

User = get_user_model()


class RegisterTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()

    def test_registration(self):
        data = {
            'email': 'new_test_user@gmail.com',
            'password': '12345678',
            'password_confirm': '12345678',
            'name': 'test'
        }

        request = self.factory.post('api/v1/account/register/', data, format='json')
        view = RegisterView.as_view()
        response = view(request)
        assert User.objects.filter(email=data['email']).exists()


class AuthenticationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.user = User.objects.create_user(
            email='user@gmail.com',
            password='12345678',
            is_active=True,
            activation_code='1234'
        )

    def test_change_password(self):
        data = {
            'old_password': '12345678',
            'new_password': '1234567a',
            'new_password_confirm': '1234567a'
        }
        request = self.factory.post('change-password/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_forgot_password(self):
        request = self.factory.post('forgot-password/', data={'email': 'user@gmail.com'}, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_forgot_password_complete(self):
        data = {
            'email': 'user@gmail.com',
            'code': '1234',
            'password': '1234test',
            'password_confirm': '1234test'
        }

        request = self.factory.post('forgot-password-complete/', data, format='json')
        view = ForgotPasswordCompleteView.as_view()
        response = view(request)
        assert response.status_code == 400
