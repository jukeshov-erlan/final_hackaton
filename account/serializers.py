from rest_framework import serializers
from django.contrib.auth import get_user_model
# from .utils import send_activation_code
from .tasks import send_activation_code_celery
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import authenticate


User = get_user_model()

# class UserSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)

#     def get_user(self, validated_data):
#         email = validated_data.get('email')
#         password = validated_data.get('password')
#         request = self.context.get('request')
#         user = authenticate(request, email=email, password=password)
#         return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(max_length=4, required=True, write_only=True)

    class Meta:
        model = User
        fields = 'email', 'password', 'password_confirm'

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Password don\'t match')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user