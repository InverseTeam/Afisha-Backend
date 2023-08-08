# Generated by Django 3.2.18 on 2023-08-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_alter_event_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название условия')),
            ],
            options={
                'verbose_name': 'Условие входа',
                'verbose_name_plural': 'Условия входа',
            },
        ),
    ]