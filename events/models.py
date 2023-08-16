import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


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
    address = models.TextField(blank=True, null=True, verbose_name='Адресс')
    location_data = models.JSONField(blank=True, null=True, verbose_name='2GIS данные')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


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
    tags = models.ManyToManyField('Tag', blank=True, related_name='events_tag', verbose_name='Тэги')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    age_limit = models.IntegerField(default=0, blank=True, verbose_name='Возрастное орграничение')
    price = models.IntegerField(default=0, blank=True, verbose_name='Цена')
    total_tickets = models.IntegerField(default=0, blank=True, verbose_name='Количество билетов')
    images = models.ManyToManyField('EventImage', blank=True, related_name='events_image', verbose_name='Фотографии мероприятия')
    date = models.DateField(blank=True, null=True, verbose_name='Дата')
    time = models.TimeField(blank=True, null=True, verbose_name='Время')
    artist = models.CharField(default='', blank=True, max_length=256, verbose_name='Артист')
    platform = models.ForeignKey('Platform', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Площадка')
    pushkin_payment = models.BooleanField(default=False, verbose_name='Оплата по пушкинской')
    want_pushkin = models.IntegerField(default=0, blank=True, verbose_name='Хочу по пушкинской')
    published = models.BooleanField(default=True, verbose_name='Опубликовано')
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


@receiver(pre_delete, sender=Event)
def event_model_delete(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete(False)

    