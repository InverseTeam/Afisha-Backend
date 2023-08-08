# Generated by Django 3.2.18 on 2023-08-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_event_entry_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default=1, max_length=256, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='open',
            field=models.BooleanField(blank=True, default=True, verbose_name='Событие открыто'),
        ),
    ]