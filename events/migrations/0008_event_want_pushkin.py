# Generated by Django 3.2.18 on 2023-08-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_alter_platform_location_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='want_pushkin',
            field=models.IntegerField(blank=True, default=0, verbose_name='Хочу по пушкинской'),
        ),
    ]
