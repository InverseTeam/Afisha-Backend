from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_currentuser.db.models import CurrentUserField
from users.models import Artist


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Platform(models.Model):
    name = models.CharField(max_length=256, verbose_name='Площадка')
    description = models.TextField(verbose_name='Описание')
    location = models.TextField(verbose_name='Расположение')
    support_phone = models.CharField(max_length=100, verbose_name='Телефон поддержки')

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


class Comment(models.Model):
    user = CurrentUserField(verbose_name='Авор')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    comment_text = models.TextField(verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Event(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    cover = models.ImageField(blank=True, null=True, upload_to='events/images/', verbose_name='Баннер')
    category = models.ForeignKey('Category', blank=True, on_delete=models.DO_NOTHING, verbose_name='Категория')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')
    description = models.TextField(verbose_name='Описание')
    age_limit = models.IntegerField(default=0, verbose_name='Возрастное орграничение')
    artists = models.ManyToManyField(Artist, blank=True, related_name='events_artist', verbose_name='Артисты')
    platform = models.ForeignKey('Platform', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Площадка')
    video = models.TextField(blank=True, null=True, verbose_name='Ссылка на видео')
    price = models.IntegerField(default=0, verbose_name='Цена')
    persons_limit = models.IntegerField(blank=True, null=True, verbose_name='Максимальное количество человек')
    open = models.BooleanField(default=True, verbose_name='Событие открыто')
    comments = models.ManyToManyField('Comment', blank=True, related_name='events_comment', verbose_name='Комментарии')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
