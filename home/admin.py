from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.AppUsage)
admin.site.register(models.NetworkTraffic)
admin.site.register(models.DeviceAvailability)
admin.site.register(models.ConnectedDevice)
admin.site.register(models.TracerouteHop)
admin.site.register(models.SystemUsage)
admin.site.register(models.Notification)