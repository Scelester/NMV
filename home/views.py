from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings


import uuid
from datetime import datetime, timedelta
from collections import defaultdict
import psutil
from ping3 import ping
import nmap
import re

from .models import NetworkTraffic, DeviceAvailability, ConnectedDevice, AppUsage, TracerouteHop, SystemUsage, Notification,UserProfile
from user_settings.models import AlertSettings,NetworkIPSetting
from .forms import CustomUserCreationForm

from .utils.traceroute import perform_traceroute



nm = nmap.PortScanner()


def sanitize_cache_key(key):
    # Replace problematic characters with '_'
    return re.sub(r'[^a-zA-Z0-9_]', '_', key)

def store_notification(user, subject, message, cooldown=100):
    now = timezone.now()

    # Create a sanitized cache key
    cache_key = sanitize_cache_key(f"notification_{user.id}_{subject}")
    last_notification_time = cache.get(cache_key)

    if last_notification_time and now - last_notification_time < timedelta(seconds=cooldown):
        return

    # Create and save the notification
    Notification.objects.create(
        user=user,
        subject=subject,
        message=message,
        created_at=now,
        last_notification_time=now,
        seen=False
    )
    
    # Update cache with the sanitized key
    cache.set(cache_key, now, timeout=cooldown)

def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, seen=False)
    

    notifications_data = [
        {
            'id': notification.id,
            'subject': notification.subject,
            'message': notification.message,
            'created_at': notification.created_at.isoformat(),
        }
        for notification in notifications
    ]

    # Update notifications to seen
    notifications.update(seen=True)

    return JsonResponse(notifications_data, safe=False)





def send_verification_email(user, request):
    token = str(uuid.uuid4())
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.verification_token = token
    user_profile.save()

    subject = 'Verify Your Email Address'
    html_message = render_to_string('email/verification_email.html', {
        'user': user,
        'token': token,
        'domain': get_current_site(request).domain,
        'protocol': 'https' if request.is_secure() else 'http',
    })
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=html_message
    )



def verify_email(request):
    token = request.GET.get('token')
    if token:
        try:
            user_profile = UserProfile.objects.get(verification_token=token)
            user_profile.email_verified = True
            user_profile.verification_token = ''
            user_profile.save()
            messages.success(request, 'Email verified successfully. You can now log in.')
            return redirect('auth')  # Redirect to login or dashboard
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid verification link.')
    else:
        messages.error(request, 'No token provided.')
    return redirect('auth')



def dashboard(request):
    return render(request, 'home/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('auth')


def auth_view(request):
    if request.user.is_authenticated:
        if not request.user.userprofile.email_verified:
            messages.warning(request, 'Please verify your email address before logging in.')
            return redirect('auth')  # Redirect to login or another page
        return redirect('dashboard')

    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()  # Use the custom form

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user.userprofile.email_verified:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Please verify your email address before logging in.')
            else:
                messages.error(request, 'Invalid username or password.')
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                send_verification_email(user, request)
                messages.success(request, 'Account created successfully! Please check your email to verify your account.')
                return redirect('auth')
            else:
                messages.error(request, 'Error creating account.')

    return render(request, 'home/login.html', {
        'login_form': login_form,
        'register_form': register_form
    })

def network_traffic(request):
    user = request.user

    # Attempt to get AlertSettings; handle the case where it does not exist
    try:
        alert_settings = AlertSettings.objects.get(user=user)
    except AlertSettings.DoesNotExist:
        alert_settings = None

    net_io = psutil.net_io_counters()
    
    

    # Convert network traffic data from bytes to GB
    bytes_sent_gb = net_io.bytes_sent / (1024 * 1024 * 1024)
    bytes_recv_gb = net_io.bytes_recv / (1024 * 1024 * 1024)

    data = {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'bytes_sent_gb': bytes_sent_gb,
        'bytes_recv_gb': bytes_recv_gb,
    }

    # Check thresholds and send notifications if needed
    if alert_settings:
        # Convert thresholds from GB to bytes
        sent_threshold_bytes = alert_settings.network_traffic_sent_threshold * 1024 * 1024 * 1024
        received_threshold_bytes = alert_settings.network_traffic_received_threshold * 1024 * 1024 * 1024

        if alert_settings.network_traffic_sent_notification and net_io.bytes_sent > sent_threshold_bytes:
        
            store_notification(
                user,
                'Network Traffic Sent Alert',
                f'Your network traffic sent has exceeded the threshold: {bytes_sent_gb:.2f} GB',
                cooldown=100
            )

        if alert_settings.network_traffic_received_notification and net_io.bytes_recv > received_threshold_bytes:
            store_notification(
                user,
                'Network Traffic Received Alert',
                f'Your network traffic received has exceeded the threshold: {bytes_recv_gb:.2f} GB',
                cooldown=100
            )
    
    # Save to database
    NetworkTraffic.objects.create(
        bytes_sent=net_io.bytes_sent,
        bytes_received=net_io.bytes_recv
    )
    
    return JsonResponse(data)




def ping_device(host):
    try:
        response_time = ping(host)
        if response_time is None:
            return False, 100, None
        else:
            response_time_ms = response_time * 1000
            packet_loss = 0
            return True, packet_loss, response_time_ms
    except Exception:
        return False, 100, None


def device_availability(request):
    user = request.user

    try:
        alert_settings = AlertSettings.objects.get(user=user)
    except AlertSettings.DoesNotExist:
        alert_settings = None

    devices = {
        'Google DNS 8.8.8.8': '8.8.8.8',
        'Google Secondary DNS 8.8.4.4': '8.8.4.4',
        'Cloudflare DNS 1.1.1.1': '1.1.1.1',
    }
    
    status = {}
    for name, ip in devices.items():
        is_available, packet_loss, ping_time = ping_device(ip)
        status[name] = {
            'online': is_available,
            'packet_loss': packet_loss,
            'ping_time': ping_time if ping_time is not None else 'N/A'
        }
        
        # Save to database
        DeviceAvailability.objects.create(
            device_name=name,
            online=is_available,
            packet_loss=packet_loss,
            ping_time=ping_time
        )

        # Check thresholds and send notifications if needed
        if alert_settings:
            if alert_settings.device_availability_packet_loss_notification and packet_loss > alert_settings.device_availability_packet_loss_threshold:
                store_notification(
                    user,
                    'Device Availability Packet Loss Alert',
                    f'{name} has exceeded the packet loss threshold: {packet_loss}%',
                )

            if alert_settings.device_availability_ping_time_notification and ping_time is not None and ping_time > alert_settings.device_availability_ping_time_threshold:
                store_notification(
                    user,
                    'Device Availability Ping Time Alert',
                    f'{name} has exceeded the ping time threshold: {ping_time} ms',
                )
    
    return JsonResponse(status)



def scan_network(ip_range):
    nm.scan(hosts=ip_range, arguments='-sn')
    devices = []
    for host in nm.all_hosts():
        devices.append({
            'ip': host,
            'ping_time': 'N/A'  # Ping time not directly available
        })
    return devices


def list_connected_devices(request):
    network_settings = get_object_or_404(NetworkIPSetting, user=request.user)
    ip_address = network_settings.ip
    subnet_prefix = network_settings.subnet
    ip_range = f"{ip_address}/{subnet_prefix}"
    devices = scan_network(ip_range)

    

    # Count the number of devices found
    device_count = len(devices)
    
    # Get alert settings for the current user
    user = request.user
    try:
        alert_settings = AlertSettings.objects.get(user=user)
    except AlertSettings.DoesNotExist:
        alert_settings = None

    # Check if we need to send a notification based on the device count
    if alert_settings and alert_settings.connected_device_count_notification:
        if device_count > alert_settings.connected_device_count_threshold:
            store_notification(
                user,
                'Connected Device Count Alert',
                f'The number of connected devices has exceeded the threshold: {device_count} devices'
            )

    # Save the devices to the database
    ConnectedDevice.objects.bulk_create(
        [ConnectedDevice(ip_address=device['ip']) for device in devices]
    )


    return JsonResponse(devices, safe=False)


def get_network_usage_by_app():
    network_info = []
    for conn in psutil.net_connections(kind='inet'):
        try:
            process = psutil.Process(conn.pid)
            app_name = process.name()
            app_id = process.pid
            local_address = conn.laddr
            remote_address = conn.raddr
            status = conn.status

            network_info.append({
                'app_name': app_name,
                'app_id': app_id,
                'local_address': f"{local_address.ip}:{local_address.port}",
                'remote_address': f"{remote_address.ip}:{remote_address.port}" if remote_address else "N/A",
                'status': status
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    app_usage = {}
    for info in network_info:
        app_id = info['app_id']
        if app_id not in app_usage:
            app_usage[app_id] = {
                'app_name': info['app_name'],
                'app_id': app_id,
                'local_address': info['local_address'],
                'remote_address': info['remote_address'],
                'status': info['status'],
                'connections': 0
            }
        app_usage[app_id]['connections'] += 1

    sorted_apps = sorted(app_usage.values(), key=lambda x: x['connections'], reverse=True)
    
    # Save to database
    AppUsage.objects.bulk_create(
        [AppUsage(
            app_name=app['app_name'],
            app_id=app['app_id'],
            local_address=app['local_address'],
            remote_address=app['remote_address'],
            status=app['status'],
            connections=app['connections']
        ) for app in sorted_apps]
    )
    
    return sorted_apps[:10]


def network_usage_by_app(request):
    data = get_network_usage_by_app()
    return JsonResponse(data, safe=False)


def get_network_usage_by_ip():
    usage = defaultdict(int)
    for conn in psutil.net_connections(kind='inet'):
        remote_ip = conn.raddr.ip if conn.raddr else None
        if remote_ip:
            usage[remote_ip] += 1

    sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
    return sorted_usage[:10]


def network_usage_by_ip(request):
    data = get_network_usage_by_ip()
    return JsonResponse(data, safe=False)


def traceroute_view(request):
    target = request.GET.get('host', 'google.com')  
    hops = perform_traceroute(target)
    
    # Save to database
    TracerouteHop.objects.bulk_create(
        [TracerouteHop(
            hop_number=hop['hop'],
            hostname=hop['hostname'],
            address=hop['address'],
            latencies=hop['latencies']
        ) for hop in hops]
    )
    
    return JsonResponse(hops, safe=False)


def system_usage_data(request):
    user = request.user

    # Get alert settings for the current user
    try:
        alert_settings = AlertSettings.objects.get(user=user)
    except AlertSettings.DoesNotExist:
        alert_settings = None

    # Measure system usage
    initial_cpu_load = psutil.cpu_percent(interval=1)
    cpu_load = initial_cpu_load * 3
    if cpu_load > 90:
        cpu_load = initial_cpu_load
    memory = psutil.virtual_memory()
    memory_used = memory.used
    memory_total = memory.total
    memory_percent = memory.percent

    # Save system usage to database
    SystemUsage.objects.create(
        cpu_load=cpu_load,
        memory_used=round(memory_used / (1024 ** 3), 2),  # Convert to GB
        memory_total=round(memory_total / (1024 ** 3), 2),  # Convert to GB
        memory_percent=memory_percent,
    )

    # Prepare response data
    data = {
        'cpu_load': cpu_load,
        'memory_used': round(memory_used / (1024 ** 3), 2),  # Convert to GB
        'memory_total': round(memory_total / (1024 ** 3), 2),  # Convert to GB
        'memory_percent': memory_percent,
    }

    # Check thresholds and send notifications if needed
    if alert_settings:
        if alert_settings.cpu_load_notification and cpu_load > alert_settings.cpu_load_threshold:
            store_notification(
                user,
                'CPU Load Alert',
                f'Your CPU load has exceeded the threshold: {cpu_load:.2f}%'
            )

        if alert_settings.memory_used_notification and memory_used > alert_settings.memory_used_threshold * (1024 ** 3):
            store_notification(
                user,
                'Memory Used Alert',
                f'Your memory usage has exceeded the threshold: {round(memory_used / (1024 ** 3), 2)} GB'
            )

        if alert_settings.memory_percent_notification and memory_percent > alert_settings.memory_percent_threshold:
            store_notification(
                user,
                'Memory Percent Alert',
                f'Your memory usage percentage has exceeded the threshold: {memory_percent:.2f}%'
            )

    return JsonResponse(data)