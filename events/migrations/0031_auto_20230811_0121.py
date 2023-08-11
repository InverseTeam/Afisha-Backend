# Generated by Django 3.2.18 on 2023-08-10 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0030_ticket_performance'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип артиста',
                'verbose_name_plural': 'Типы артистов',
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100, verbose_name='Псевдоним')),
                ('bio', models.TextField(verbose_name='Описание')),
                ('firstname', models.CharField(max_length=100, verbose_name='Имя')),
                ('lastname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('surname', models.CharField(max_length=100, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='День рождения')),
                ('artist_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artists_artisttype', to='events.artisttype', verbose_name='Тип артиста')),
                ('manager', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер')),
            ],
            options={
                'verbose_name': 'Артист',
                'verbose_name_plural': 'Артисты',
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='artists',
            field=models.ManyToManyField(blank=True, related_name='events_artist', to='events.Artist', verbose_name='Артисты'),
        ),
    ]