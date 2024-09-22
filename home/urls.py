from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('network-traffic/', views.network_traffic, name='network_traffic'),
    path('device-availability/', views.device_availability, name='device_availability'),
    path('connected-devices/', views.list_connected_devices, name='list_connected_devices'),
    path('network-usage/', views.network_usage_by_app, name='network_usage_by_app'),
    path('network-usage-by-ip/', views.network_usage_by_ip, name='network_usage_by_ip'),
    path('trace-route/', views.traceroute_view, name='trace_route'),
    path('api/system-usage/', views.system_usage_data, name='system_usage_data'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('verify-email/', views.verify_email, name='verify_email'),
]