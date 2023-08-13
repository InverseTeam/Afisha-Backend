import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django_currentuser.db.models import CurrentUserField
from users.models import CustomUser, Role


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Platform(models.Model):
    name = models.CharField(max_length=256, verbose_name='Площадка')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    location = models.TextField(blank=True, null=True, verbose_name='Расположение')
    support_phone = models.CharField(default='', blank=True, max_length=100, verbose_name='Телефон поддержки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


class Ticket(models.Model):
    user = CurrentUserField(related_name='tickets_user', verbose_name='Покупатель')
    attended = models.BooleanField(default=False, blank=True, verbose_name='Посетил')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


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
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    age_category = models.ForeignKey(Role, blank=True, null=True, related_name='events_role', on_delete=models.DO_NOTHING, verbose_name='Возрастная категория')
    platform = models.ForeignKey('Platform', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Площадка')
    images = models.ManyToManyField('EventImage', blank=True, related_name='events_image', verbose_name='Фотографии мероприятия')
    comments = models.ManyToManyField('Comment', blank=True, related_name='events_comment', verbose_name='Комментарии')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата конца')
    tickets_number = models.IntegerField(default=0, blank=True, verbose_name='Количество билетов')
    tickets_sold = models.IntegerField(default=0, blank=True, verbose_name='Билетов продано')
    tickets = models.ManyToManyField('Ticket', blank=True, related_name='events_ticket', verbose_name='Билеты')
    published = models.BooleanField(default=False, blank=True, verbose_name='Событие опубликовано')
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


# @receiver(pre_delete, sender=Event)
# def event_model_delete(sender, instance, **kwargs):
#     if instance.cover:
#         instance.cover.delete(False)


#     if instance.comments.all():
#         for comment in instance.comments.all():
#             comment.delete()

    