# Generated by Django 5.0.7 on 2024-09-04 07:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0005_networkipsetting'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkipsetting',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='network_ip_setting', to=settings.AUTH_USER_MODEL),
        ),
    ]
