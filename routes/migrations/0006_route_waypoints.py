# Generated by Django 3.2.18 on 2023-08-04 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_auto_20230804_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='waypoints',
            field=models.JSONField(blank=True, null=True, verbose_name='Маршруты'),
        ),
    ]
