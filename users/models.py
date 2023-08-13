from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_currentuser.db.models import CurrentUserField


class Role(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    role_type = models.CharField(max_length=100, verbose_name='Тип роли')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(blank=True, null=True, verbose_name='Почта')
    firstname = models.CharField(max_length=256, blank=True, verbose_name='Имя')
    lastname = models.CharField(max_length=256, blank=True, verbose_name='Фамилия')
    role = models.ForeignKey('Role', default=1, on_delete=models.CASCADE, related_name='users_role', verbose_name='Роль')
    password = models.CharField(max_length=256, verbose_name='Пароль')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
