from django.db import models
from django.contrib.auth.models import User

class AlertSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alert_settings')

    # Thresholds with corresponding notification flags
    cpu_load_threshold = models.FloatField(default=80.0)  # Default threshold
    cpu_load_notification = models.BooleanField(default=True)

    memory_used_threshold = models.BigIntegerField(default=8)  # Default threshold in bytes (8 GB)
    memory_used_notification = models.BooleanField(default=True)

    memory_percent_threshold = models.FloatField(default=80.0)  # Default threshold
    memory_percent_notification = models.BooleanField(default=True)

    network_traffic_sent_threshold = models.BigIntegerField(default=1)  # Default threshold in bytes (1 GB)
    network_traffic_sent_notification = models.BooleanField(default=True)

    network_traffic_received_threshold = models.BigIntegerField(default=10)  # Default threshold in bytes (10 GB)
    network_traffic_received_notification = models.BooleanField(default=True)

    device_availability_packet_loss_threshold = models.FloatField(default=50.0)  # Default threshold in percentage
    device_availability_packet_loss_notification = models.BooleanField(default=True)

    device_availability_ping_time_threshold = models.FloatField(default=150.0)  # Default threshold in ms
    device_availability_ping_time_notification = models.BooleanField(default=True)

    connected_device_count_threshold = models.IntegerField(default=40)  # Default threshold
    connected_device_count_notification = models.BooleanField(default=True)

    def __str__(self):
        return f"Alert settings for {self.user.username}"


class NetworkIPSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='network_ip_setting')
    ip = models.CharField(max_length=20, default="192.168.1.0")
    subnet = models.IntegerField(default=24)

    def __str__(self):
        return f"{self.user.username}'s Network Settings"