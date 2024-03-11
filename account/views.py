from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import Throttled
from account.throttle import UserLoginRateThrottle
from django.conf import settings
from django.shortcuts import render


def demo_recaptcha(request):
    return render(request, 'demo_recaptcha.html', {
        "key": settings.RE_CAPTCHA_SITE_KEY
    })



class RegisterView(APIView):
    throttle_classes = (UserLoginRateThrottle,)

    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Аккаунт успешно создан', status=201)

    def perform_create(self, serializer):
        user = serializer.save()

    def throttled(self, request, wait):
        raise Throttled(detail={
            "message": "recaptcha_required",
        })



class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
        return Response(
            'Аккаунт успешно активирован',
            status=200
        )


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно вышли из аккаунта', status=204)


class ChangePasswordVIew(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response(
            'Пароль успешно изменен', status=200
        )


class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_verification_email()
        return Response('Сообщение для восстановления отправлено на почту', status=200)
    

class ForgotPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Вы успешно обновили пароль', status=200)
