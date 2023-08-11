import uuid
from django.db import models
from users.models import CustomUser


class RouteType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    query_text = models.TextField(verbose_name='Текст 2GIS запроса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип маршрута'
        verbose_name_plural = 'Типы маршрутов'


class Route(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'routes/covers/{image_uuid}.{extension}'

    name = models.CharField(max_length=256, verbose_name='Маршрут')
    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Баннер')
    duration = models.IntegerField(blank=True, null=True, verbose_name='Длительность')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата конца')
    price = models.IntegerField(default=0, blank=True, verbose_name='Цена')
    age_limit = models.IntegerField(blank=True, null=True, verbose_name='Возрастное ограничение')
    route_type = models.ForeignKey('RouteType', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Тип маршрута')
    active = models.BooleanField(default=True, blank=True, verbose_name='Активный отдых')
    waypoints = models.JSONField(blank=True, null=True, verbose_name='Маршруты')
    tickets = models.ManyToManyField(CustomUser, blank=True, related_name='routes_user', verbose_name='Билеты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'