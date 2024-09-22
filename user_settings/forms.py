from django.db import models
from django import forms
from django.contrib.auth.models import User
from .models import AlertSettings,NetworkIPSetting

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

class AlertSettingsForm(forms.ModelForm):
    class Meta:
        model = AlertSettings
        fields = [
            'cpu_load_threshold', 'cpu_load_notification',
            'memory_used_threshold', 'memory_used_notification',
            'memory_percent_threshold', 'memory_percent_notification',
            'network_traffic_sent_threshold', 'network_traffic_sent_notification',
            'network_traffic_received_threshold', 'network_traffic_received_notification',
            'device_availability_packet_loss_threshold', 'device_availability_packet_loss_notification',
            'device_availability_ping_time_threshold', 'device_availability_ping_time_notification',
            'connected_device_count_threshold', 'connected_device_count_notification',
        ]
        widgets = {
            'cpu_load_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'memory_used_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'memory_percent_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'network_traffic_sent_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'network_traffic_received_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'device_availability_packet_loss_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'device_availability_ping_time_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'connected_device_count_threshold': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'cpu_load_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'memory_used_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'memory_percent_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'network_traffic_sent_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'network_traffic_received_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'device_availability_packet_loss_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'device_availability_ping_time_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'connected_device_count_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(AlertSettingsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'step': 'any'})  # Allow decimal inputs

class NetworkIPSettingForm(forms.ModelForm):
    class Meta:
        model = NetworkIPSetting
        fields = ['ip', 'subnet']

    def __init__(self, *args, **kwargs):
        super(NetworkIPSettingForm, self).__init__(*args, **kwargs)
        # Adding styles to 'ip' field
        self.fields['ip'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter IP Address'
        })
        # Adding styles to 'subnet' field
        self.fields['subnet'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '',
            'min': 0, 
            'max': 32  
        })
        self.fields['subnet'].label = 'Subnet Prefix Length'