import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_currentuser.db.models import CurrentUserField
from users.models import Artist, CustomUser


class EntryCondition(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название условия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Условие входа'
        verbose_name_plural = 'Условия входа'


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Platform(models.Model):
    name = models.CharField(max_length=256, verbose_name='Площадка')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    location = models.TextField(blank=True, null=True, verbose_name='Расположение')
    support_phone = models.CharField(max_length=100, verbose_name='Телефон поддержки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


class Comment(models.Model):
    user = CurrentUserField(verbose_name='Авор')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    comment_text = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class EventImage(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        uuid = uuid.uuid1().hex
        return f'events/images/{uuid}.{extension}'
    
    image = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Баннер')

    class Meta:
        verbose_name = 'Файл события'
        verbose_name_plural = 'Файлы события'


class Event(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'events/covers/{image_uuid}.{extension}'
    
    name = models.CharField(default='', max_length=256, verbose_name='Название')
    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Баннер')
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Категория')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    age_limit = models.IntegerField(default=0, verbose_name='Возрастное орграничение')
    artists = models.ManyToManyField(Artist, blank=True, related_name='events_artist', verbose_name='Артисты')
    platform = models.ForeignKey('Platform', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Площадка')
    video = models.TextField(blank=True, null=True, verbose_name='Ссылка на видео')
    images = models.ManyToManyField('EventImage', blank=True, related_name='events_image', verbose_name='Фотографии мероприятия')
    price = models.IntegerField(default=0, verbose_name='Цена')
    total_tickets = models.IntegerField(blank=True, null=True, verbose_name='Всего билетов')
    tickets = models.ManyToManyField(CustomUser, blank=True, related_name='events_user', verbose_name='Билеты')
    open = models.BooleanField(default=True, blank=True, verbose_name='Событие открыто')
    comments = models.ManyToManyField('Comment', blank=True, related_name='events_comment', verbose_name='Комментарии')
    when = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время')
    entry_condition = models.ForeignKey('EntryCondition', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Условия входа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'



