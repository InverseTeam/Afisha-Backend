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


class TicketType(models.Model):
    sector = models.CharField(default='Зал', max_length=255, verbose_name='Сектор')
    price = models.IntegerField(default=0, verbose_name='Цена')
    tickets_number = models.IntegerField(default=0, verbose_name='Количество билетов')
    tickets_sold = models.IntegerField(default=0, verbose_name='Билетов продано')
    open = models.BooleanField(default=True, blank=True, verbose_name='Открыто')

    def __str__(self):
        return self.sector

    class Meta:
        verbose_name = 'Тип билета'
        verbose_name_plural = 'Типы билетов'


class Ticket(models.Model):
    buyer = CurrentUserField(related_name='tickets_user', verbose_name='Покупатель')
    ticket_type = models.ForeignKey('TicketType', related_name='tickets_tickettype', on_delete=models.DO_NOTHING, verbose_name='Тип билета')

    def __str__(self):
        return self.buyer.email

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


class Performance(models.Model):
    name = models.CharField(default='Выступление', max_length=255, verbose_name='Название выступления')
    time = models.TimeField(blank=True, null=True, verbose_name='Время')
    date = models.DateField(blank=True, null=True, verbose_name='Дата')
    ticket_types = models.ManyToManyField('TicketType', blank=True, related_name='performances_tickettype', verbose_name='Типы билетов')
    tickets = models.ManyToManyField('Ticket', blank=True, related_name='performance_ticket', verbose_name='Билеты')
    open = models.BooleanField(default=True, blank=True, verbose_name='Открыто')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date']
        verbose_name = 'Выступление'
        verbose_name_plural = 'Выступления'


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
    age_limit = models.IntegerField(default=0, verbose_name='Возрастное орграничение')
    platform = models.ForeignKey('Platform', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Площадка')
    performances = models.ManyToManyField('Performance', blank=True, related_name='events_performance', verbose_name='Выступления')
    video = models.TextField(blank=True, null=True, verbose_name='Ссылка на видео')
    images = models.ManyToManyField('EventImage', blank=True, related_name='events_image', verbose_name='Фотографии мероприятия')
    comments = models.ManyToManyField('Comment', blank=True, related_name='events_comment', verbose_name='Комментарии')
    entry_condition = models.ForeignKey('EntryCondition', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Условия входа')
    artists = models.ManyToManyField(Artist, blank=True, related_name='events_artist', verbose_name='Артисты')
    manager = CurrentUserField(related_name='events_manager', verbose_name='Менеджер')
    open = models.BooleanField(default=True, blank=True, verbose_name='Событие открыто')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата конца')
    tickets_number = models.IntegerField(default=0, verbose_name='Количество билетов')
    tickets_sold = models.IntegerField(default=0, verbose_name='Билетов продано')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'