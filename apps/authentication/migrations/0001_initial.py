# Generated by Django 4.2 on 2024-01-23 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refresh_token', models.CharField(max_length=1000, verbose_name='refresh_token')),
                ('expired_at', models.DateTimeField(verbose_name='expired at')),
                ('device_name', models.CharField(max_length=244, verbose_name='device name')),
                ('ip_address', models.GenericIPAddressField(verbose_name='ip address')),
                ('last_login', models.DateTimeField(verbose_name='last login')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logins', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User Login',
                'verbose_name_plural': 'User Logins',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
