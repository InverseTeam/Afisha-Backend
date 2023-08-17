# Generated by Django 3.2.18 on 2023-08-16 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='adress',
            field=models.TextField(blank=True, null=True, verbose_name='Адресс'),
        ),
        migrations.AlterField(
            model_name='event',
            name='artist',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Артист'),
        ),
    ]