from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_currentuser.db.models import CurrentUserField


class ArtistType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'


class Artist(models.Model):
    nickname = models.CharField(max_length=100, verbose_name='Псевдоним')
    bio = models.TextField(verbose_name='Описание')
    firstname = models.CharField(max_length=100, verbose_name='Имя')
    lastname = models.CharField(max_length=100, verbose_name='Фамилия')
    surname = models.CharField(max_length=100, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='День рождения')
    artist_type = models.ForeignKey('ArtistType', blank=True, null=True, on_delete=models.CASCADE, related_name='artists_artisttype', verbose_name='Тип артиста')
    manager = CurrentUserField(verbose_name='Автор курса')

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'


class Role(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    role_id = models.IntegerField(verbose_name='ID')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Username must be set')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=50, blank=True, verbose_name='Номер телефона')
    firstname = models.CharField(max_length=256, blank=True, verbose_name='Имя')
    lastname = models.CharField(max_length=256, blank=True, verbose_name='Фамилия')
    role = models.ForeignKey('Role', default=1, on_delete=models.CASCADE, related_name='users_role', verbose_name='Роль')
    age = models.IntegerField(blank=True, null=True, verbose_name='Возраст')
    password = models.CharField(max_length=256, verbose_name='Пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
