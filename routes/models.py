import uuid
from django.db import models
from users.models import CustomUser


class Route(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'routes/covers/{image_uuid}.{extension}'

    name = models.CharField(max_length=256, verbose_name='Маршрут')
    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Баннер')
    waypoints = models.JSONField(blank=True, null=True, verbose_name='Маршруты')
    tickets = models.ManyToManyField(CustomUser, blank=True, related_name='routes_user', verbose_name='Билеты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'