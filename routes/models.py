import random 
from django.db import models
from django_currentuser.db.models import CurrentUserField
from events.models import Event
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from routes.gis import get_route


class CustomRoute(models.Model):
    user = CurrentUserField(verbose_name='Создатель маршрута')
    duration = models.IntegerField(blank=True, verbose_name='Длительность')
    distance = models.IntegerField(blank=True, verbose_name='Протяжённость')
    waypoints = models.ManyToManyField(Event, blank=True, related_name='customroutes_event', verbose_name='Точки маршрута')

    class Meta:
        verbose_name = 'Кастомный маршрут'        
        verbose_name_plural = 'Кастомные маршруты'


class Route(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    duration = models.IntegerField(blank=True, null=True, verbose_name='Длительность')
    distance = models.IntegerField(blank=True, null=True, verbose_name='Протяжённость')
    waypoints = models.ManyToManyField(Event, blank=True, related_name='routes_event', verbose_name='Точки маршрута')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


@receiver(pre_save, sender=Route)
def get_route_metrics(sender, instance, **kwargs):
    route_duration = random.randint(80, 240)
    instance.duration = route_duration
    instance.distance = route_duration / 60 * 5


@receiver(pre_save, sender=CustomRoute)
def get_route_metrics(sender, instance, **kwargs):
    route_duration = random.randint(80, 240)
    instance.duration = route_duration
    instance.distance = route_duration / 60 * 5
