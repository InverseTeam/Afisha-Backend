# Generated by Django 3.2.18 on 2023-08-16 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_rename_adress_platform_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='location_data',
            field=models.JSONField(blank=True, null=True, verbose_name='2GIS данные'),
        ),
    ]
