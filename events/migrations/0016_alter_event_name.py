# Generated by Django 3.2.18 on 2023-08-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20230806_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=256, verbose_name='Название'),
        ),
    ]