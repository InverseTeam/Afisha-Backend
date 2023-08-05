# Generated by Django 3.2.18 on 2023-08-03 13:25

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230803_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='manager',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
    ]
