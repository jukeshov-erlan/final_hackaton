from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer # UserSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema



class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Successfully registered', status=201)


# class TokenObtainView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data
#         user = serializer.get_user(validated_data)
#         refresh = RefreshToken.for_user(user)
#         access_token = refresh.access_token
#         return Response({
#             'refresh': str(refresh),
#             'access': str(access_token)
#         })


class ActivateView(APIView):
    def get(self, request, email, activation_code):
        user = get_user_model().objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated', 200)
