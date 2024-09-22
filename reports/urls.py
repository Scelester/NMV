from django.urls import path
from . import views

urlpatterns = [
    path('', views.history_overview, name='history_overview'),
    path('networktraffic/', views.history_networktraffic, name='history_networktraffic'),
    path('deviceavailability/', views.device_availability_history, name='history_deviceavailability'),
    path('connecteddevice/', views.history_connecteddevice, name='history_connecteddevice'),
    path('appusage/', views.history_appusage, name='history_appusage'),
    path('systemusage/', views.system_usage_history, name='history_systemusage'),
]
