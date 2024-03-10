from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.contrib.auth import get_user_model
from .views import RegisterView, ActivateView, LogoutAPIView, ChangePasswordVIew, ForgotPasswordView, ForgotPasswordCompleteView
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class AuthTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            password='12345678',
            is_active=True,
            activation_code='1234'
        )

    def test_registration(self):
        data = {
            'email': 'new_test_user@gmail.com',
            'password': '12345678',
            'password_confirm': '12345678',
            'name': 'test'
        }

        request = self.factory.post('api/v1/account/register/', data, format='json')
        # print(request)
        # print('================')
        view = RegisterView.as_view()
        response = view(request)
        # print(response)
        # print('===========')
        assert User.objects.filter(email=data['email']).exists()
        # assert response.status_code == 201

    def test_login(self):

        data = {
            'email': 'user@gmail.com',
            'password': '12345678'
        }

        request = self.factory.post('login/', data, format='json')
        view = TokenObtainPairView.as_view()
        response = view(request)
        assert 'token' in response.data

    def test_change_password(self):
        data = {
            'old_password': '12345678',
            'new_password': '1234567a',
            'new_password_confirm': '1234567a'
        }
        request = self.factory.post('change-password/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ChangePasswordVIew.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_forgot_password(self):
        request = self.factory.post('forgot-password/', data= {'email': 'user@gmail.com'}, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_forgot_pass_complete(self):
        data ={
            'email': 'user@gmail.com', 
            'code': '1234', 
            'password': '1234test', 
            'password_confirm': '1234test'
            }
        
        request = self.factory.post('forgot-password-complete/', data, format='json')
        view = ForgotPasswordCompleteView.as_view()
        response = view(request)
        print(response.data)
        assert response.status_code == 200

