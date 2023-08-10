# Generated by Django 3.2.18 on 2023-08-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20230810_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='age_limit',
            field=models.IntegerField(blank=True, default=0, verbose_name='Возрастное орграничение'),
        ),
        migrations.AlterField(
            model_name='event',
            name='tickets_number',
            field=models.IntegerField(blank=True, default=0, verbose_name='Количество билетов'),
        ),
        migrations.AlterField(
            model_name='event',
            name='tickets_sold',
            field=models.IntegerField(blank=True, default=0, verbose_name='Билетов продано'),
        ),
    ]