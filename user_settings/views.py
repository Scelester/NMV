from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserSettingsForm, AlertSettingsForm,NetworkIPSettingForm
from .models import AlertSettings,NetworkIPSetting

@login_required
def settings_view(request):
    # Retrieve the user's alert settings or create default if none exist
    alert_settings, created = AlertSettings.objects.get_or_create(user=request.user)

    if not hasattr(request.user, 'network_ip_setting'):
        NetworkIPSetting.objects.create(user=request.user)

    if request.method == 'POST':
        # Handle user settings form
        user_form = UserSettingsForm(request.POST, instance=request.user)
        # Handle password change form
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        # Handle alert settings form
        alert_form = AlertSettingsForm(request.POST, instance=alert_settings)

        if 'username_change' in request.POST and user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your username was successfully updated!')
            return redirect('settings')

        elif 'password_change' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')

        elif 'alert_settings_change' in request.POST and alert_form.is_valid():
            alert_form.save()
            messages.success(request, 'Your alert settings were successfully updated!')
            return redirect('settings')
        if 'ip_settings_change' in request.POST:
            ipsetform = NetworkIPSettingForm(request.POST, instance=request.user.network_ip_setting)
            if ipsetform.is_valid():
                ipsetform.save()
                return redirect('settings')

    else:
        # Initialize forms with existing data for GET request
        user_form = UserSettingsForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        alert_form = AlertSettingsForm(instance=alert_settings)
        ipsetform = NetworkIPSettingForm(instance=request.user.network_ip_setting)

    context = {
        'user_form': user_form,
        'password_form': password_form,
        'alert_form': alert_form,
        'ipsetform':ipsetform
    }

    return render(request, 'user_settings/index.html', context)
