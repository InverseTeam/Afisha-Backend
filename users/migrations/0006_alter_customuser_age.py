# Generated by Django 3.2.20 on 2023-08-02 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230803_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='Возраст'),
        ),
    ]
