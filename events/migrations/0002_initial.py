# Generated by Django 3.2.18 on 2023-08-15 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets_user', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='performance',
            name='ticket_types',
            field=models.ManyToManyField(blank=True, related_name='performances_tickettype', to='events.TicketType', verbose_name='Типы билетов'),
        ),
        migrations.AddField(
            model_name='performance',
            name='tickets',
            field=models.ManyToManyField(blank=True, related_name='performance_ticket', to='events.Ticket', verbose_name='Билеты'),
        ),
        migrations.AddField(
            model_name='event',
            name='artists',
            field=models.ManyToManyField(blank=True, related_name='events_artist', to='events.Artist', verbose_name='Артисты'),
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='events.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='event',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='events_comment', to='events.Comment', verbose_name='Комментарии'),
        ),
        migrations.AddField(
            model_name='event',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='events_image', to='events.EventImage', verbose_name='Фотографии мероприятия'),
        ),
        migrations.AddField(
            model_name='event',
            name='performances',
            field=models.ManyToManyField(blank=True, related_name='events_performance', to='events.Performance', verbose_name='Выступления'),
        ),
        migrations.AddField(
            model_name='event',
            name='platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.platform', verbose_name='Площадка'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='events_tag', to='events.Tag', verbose_name='Тэги'),
        ),
        migrations.AddField(
            model_name='event',
            name='tickets',
            field=models.ManyToManyField(blank=True, related_name='events_ticket', to='events.Ticket', verbose_name='Билеты'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Авор'),
        ),
        migrations.AddField(
            model_name='category',
            name='tags',
            field=models.ManyToManyField(to='events.Tag', verbose_name='Тэги'),
        ),
        migrations.AddField(
            model_name='artist',
            name='artist_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artists_artisttype', to='events.artisttype', verbose_name='Тип артиста'),
        ),
    ]
