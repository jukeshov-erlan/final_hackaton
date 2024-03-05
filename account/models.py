from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.create_activation_code()
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatar/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'email' #field for login

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    def create_activation_code(self):
        code = get_random_string(length=10, allowed_chars='0123456789')
        self.activation_code = code
        self.save()