from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .logging import LoggingView
from .serializers import *


class RegisterView(LoggingView, APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        self.log_user_activity(request, "зарегистрировал аккаунт")  # вызываем метод логирования
        return Response('Аккаунт успешно создан', status=201)


class ActivateView(LoggingView, APIView):
    def get(self, request, email, activation_code):
        user = get_user_model().objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        self.log_user_activity(request, "активировал свой аккаунт")  # вызываем метод логирования
        return Response('Аккаунт активирован', 200)


class LogoutAPIView(LoggingView, APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.log_user_activity(request, "вышел из аккаунта")  # вызываем метод логирования
        return Response('Вы успешно вышли из аккаунта', status=204)


class ChangePasswordView(LoggingView, APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        self.log_user_activity(request, "изменил свой пароль")  # вызываем метод логирования
        return Response('Пароль успешно изменен', status=200)


class ForgotPasswordView(LoggingView, APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_verification_email()
        self.log_user_activity(request, "запросил восстановление пароля")  # вызываем метод логирования
        return Response('Сообщение для восстановления отправлено на почту', status=200)


class ForgotPasswordCompleteView(LoggingView, APIView):
    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        self.log_user_activity(request, "завершил процесс восстановления пароля")  # вызываем метод логирования
        return Response('Вы успешно обновили пароль', status=200)
