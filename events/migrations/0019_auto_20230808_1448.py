# Generated by Django 3.2.18 on 2023-08-08 09:48

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_event_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.Event.get_path, verbose_name='Баннер'),
        ),
        migrations.AlterField(
            model_name='eventimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.EventImage.get_path, verbose_name='Баннер'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='location',
            field=models.TextField(blank=True, null=True, verbose_name='Расположение'),
        ),
    ]