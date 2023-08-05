# Generated by Django 3.2.18 on 2023-08-05 08:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('routes', '0006_route_waypoints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='author',
        ),
        migrations.AddField(
            model_name='route',
            name='tickets',
            field=models.ManyToManyField(blank=True, related_name='routes_user', to=settings.AUTH_USER_MODEL, verbose_name='Билеты'),
        ),
    ]
