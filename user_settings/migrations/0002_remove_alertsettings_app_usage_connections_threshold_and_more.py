# Generated by Django 5.0.7 on 2024-08-27 02:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertsettings',
            name='app_usage_connections_threshold',
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='connected_device_count_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='cpu_load_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='device_availability_packet_loss_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='device_availability_ping_time_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='memory_percent_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='memory_used_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='network_traffic_received_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='network_traffic_sent_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alertsettings',
            name='traceroute_hop_latency_notification',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='connected_device_count_threshold',
            field=models.IntegerField(default=40),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='device_availability_packet_loss_threshold',
            field=models.FloatField(default=50.0),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='device_availability_ping_time_threshold',
            field=models.FloatField(default=150.0),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='memory_used_threshold',
            field=models.BigIntegerField(default=8589934592),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='network_traffic_received_threshold',
            field=models.BigIntegerField(default=10737418240),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='network_traffic_sent_threshold',
            field=models.BigIntegerField(default=1073741824),
        ),
        migrations.AlterField(
            model_name='alertsettings',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alert_settings', to=settings.AUTH_USER_MODEL),
        ),
    ]
