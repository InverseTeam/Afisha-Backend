# Generated by Django 3.2.18 on 2023-08-05 08:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20230804_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tickets',
            field=models.ManyToManyField(blank=True, related_name='events_user', to=settings.AUTH_USER_MODEL, verbose_name='Билеты'),
        ),
    ]