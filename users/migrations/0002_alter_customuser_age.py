# Generated by Django 3.2.20 on 2023-08-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(blank=True, verbose_name='Возраст'),
        ),
    ]
