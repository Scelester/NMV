from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

MAX_RECORDS = 5000

class NetworkTraffic(models.Model):
    bytes_sent = models.BigIntegerField()
    bytes_received = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NetworkTraffic at {self.timestamp}: Sent {self.bytes_sent} bytes, Received {self.bytes_received} bytes"

#     @classmethod
#     def post_save_handler(cls, sender, instance, created, **kwargs):
#         if created:
#             if cls.objects.count() > MAX_RECORDS:
#                 cls.objects.order_by('timestamp').first().delete()

# post_save.connect(NetworkTraffic.post_save_handler, sender=NetworkTraffic)


class DeviceAvailability(models.Model):
    device_name = models.CharField(max_length=255)
    online = models.BooleanField()
    packet_loss = models.FloatField()
    ping_time = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Online" if self.online else "Offline"
        ping_time_str = f"{self.ping_time} ms" if self.ping_time is not None else "N/A"
        return f"{self.device_name}: {status}, Packet Loss: {self.packet_loss}%, Ping Time: {ping_time_str} (at {self.timestamp})"

#     @classmethod
#     def post_save_handler(cls, sender, instance, created, **kwargs):
#         if created:
#             if cls.objects.count() > MAX_RECORDS:
#                 cls.objects.order_by('timestamp').first().delete()

# post_save.connect(DeviceAvailability.post_save_handler, sender=DeviceAvailability)


class ConnectedDevice(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ConnectedDevice {self.ip_address} at {self.timestamp}"

#     @classmethod
#     def post_save_handler(cls, sender, instance, created, **kwargs):
#         if created:
#             if cls.objects.count() > MAX_RECORDS:
#                 cls.objects.order_by('timestamp').first().delete()

# post_save.connect(ConnectedDevice.post_save_handler, sender=ConnectedDevice)


class AppUsage(models.Model):
    app_name = models.CharField(max_length=255)
    app_id = models.IntegerField()
    local_address = models.CharField(max_length=255)
    remote_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    connections = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AppUsage: {self.app_name} (ID: {self.app_id}), Local: {self.local_address}, Remote: {self.remote_address}, Status: {self.status}, Connections: {self.connections} (at {self.timestamp})"

#     @classmethod
#     def post_save_handler(cls, sender, instance, created, **kwargs):
#         if created:
#             if cls.objects.count() > MAX_RECORDS:
#                 cls.objects.order_by('timestamp').first().delete()

# post_save.connect(AppUsage.post_save_handler, sender=AppUsage)


class TracerouteHop(models.Model):
    hop_number = models.IntegerField()
    hostname = models.CharField(max_length=255)
    address = models.GenericIPAddressField()
    latencies = models.JSONField()  # Store latencies as a JSON array
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        latencies_str = ", ".join(str(latency) + " ms" for latency in self.latencies)
        return f"TracerouteHop {self.hop_number}: {self.hostname} ({self.address}), Latencies: {latencies_str} (at {self.timestamp})"

#     @classmethod
#     def post_save_handler(cls, sender, instance, created, **kwargs):
#         if created:
#             if cls.objects.count() > MAX_RECORDS:
#                 cls.objects.order_by('timestamp').first().delete()

# post_save.connect(TracerouteHop.post_save_handler, sender=TracerouteHop)



class SystemUsage(models.Model):
    cpu_load = models.FloatField()  # Store CPU load percentage
    memory_used = models.FloatField()  # Store used memory in GB
    memory_total = models.FloatField()  # Store total memory in GB
    memory_percent = models.FloatField()  # Store memory usage percentage
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CPU Load: {self.cpu_load}%, Memory Used: {self.memory_used}GB/{self.memory_total}GB ({self.memory_percent}%) at {self.timestamp}"

#     @classmethod
#     def post_save_handler(cls, sender, instance, created, **kwargs):
#         MAX_RECORDS = 5000
#         if created:
#             if cls.objects.count() > MAX_RECORDS:
#                 cls.objects.order_by('timestamp').first().delete()

# post_save.connect(SystemUsage.post_save_handler, sender=SystemUsage)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_notification_time = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Notification for {self.user.username}: {self.subject}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verified = models.BooleanField(default=False)