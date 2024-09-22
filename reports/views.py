from django.shortcuts import render
from home.models import NetworkTraffic, DeviceAvailability, ConnectedDevice, AppUsage, TracerouteHop, SystemUsage

from django.utils.dateparse import parse_datetime
# from django.db.models import Sum
# from datetime import timedelta
import json
from django.db.models import Count, Max
from django.utils.dateformat import format


def history_overview(request):
    return render(request, 'reports/index.html')


def history_networktraffic(request):
    # Fetch all data from NetworkTraffic
    network_data = NetworkTraffic.objects.all().values('timestamp', 'bytes_sent', 'bytes_received')
    
    # Convert data to lists and process
    timestamps = [data['timestamp'].strftime('%Y-%m-%d %H:%M:%S') for data in network_data]
    sent_bytes = [data['bytes_sent'] / (1024 ** 2) for data in network_data]  # Convert bytes to MB
    received_bytes = [data['bytes_received'] / (1024 ** 2) for data in network_data]  # Convert bytes to MB
    
    # Reduce the number of points if necessary (e.g., take every 10th point)
    step = max(len(timestamps) // 500, 1)  # Adjust step to limit number of points to around 500
    reduced_timestamps = timestamps[::step]
    reduced_sent_bytes = sent_bytes[::step]
    reduced_received_bytes = received_bytes[::step]
    
    context = {
        'model_name': 'Network Traffic',
        'labels': reduced_timestamps,
        'data_points': {
            'Sent_Bytes': reduced_sent_bytes,
            'Received_Bytes': reduced_received_bytes
        }
    }
    
    return render(request, 'reports/history_networktraffic.html', context)






def device_availability_history(request):
    # Get all device names
    devices = DeviceAvailability.objects.values_list('device_name', flat=True).distinct()

    # Initialize dictionaries to hold data for each device
    packet_loss_data = {}
    ping_time_data = {}

    for device in devices:
        # Query data for each device
        data = DeviceAvailability.objects.filter(device_name=device).order_by('timestamp')

        # Prepare data for packet loss
        packet_loss_data[device] = {
            'timestamps': [entry.timestamp.isoformat() for entry in data],
            'packet_loss': [entry.packet_loss for entry in data]
        }

        # Prepare data for ping time
        ping_time_data[device] = {
            'timestamps': [entry.timestamp.isoformat() for entry in data],
            'ping_time': [entry.ping_time for entry in data if entry.ping_time is not None]
        }

    context = {
        'devices': devices,
        'packet_loss_data': json.dumps(packet_loss_data),
        'ping_time_data': json.dumps(ping_time_data),
    }
    return render(request, 'reports/device_availability_history.html', context)



def history_connecteddevice(request):
    # Query to get unique IPs, count of occurrences, and the latest timestamp
    devices = (
        ConnectedDevice.objects.values('ip_address')
        .annotate(
            count=Count('ip_address'),
            latest_timestamp=Max('timestamp')
        )
        .order_by('-latest_timestamp')  # Sort by latest timestamp
    )

    context = {
        'devices': devices
    }
    return render(request, 'reports/history_connected_devices.html', context)


def history_appusage(request):
    apps = (
        AppUsage.objects.values('app_name', 'app_id', 'local_address', 'remote_address', 'status')
        .annotate(
            latest_connections=Max('connections'),
            latest_timestamp=Max('timestamp')
        )
        .order_by('-latest_timestamp')  # Sort by the latest timestamp
    )

    context = {
        'apps': apps
    }
    return render(request, 'reports/history_app_usage.html', context)


def system_usage_history(request):
    data = SystemUsage.objects.order_by('-timestamp')[:1000]
    
    timestamps = [entry.timestamp.isoformat() for entry in data]
    cpu_loads = [entry.cpu_load for entry in data]
    memory_used = [entry.memory_used for entry in data]
    memory_percent = [entry.memory_percent for entry in data]
    
    context = {
        'timestamps': json.dumps(timestamps),  # Ensure JSON format for JavaScript
        'cpu_loads': json.dumps(cpu_loads),
        'memory_used': json.dumps(memory_used),
        'memory_percent': json.dumps(memory_percent),
    }
    
    return render(request, 'reports/system_usage_history.html', context)






