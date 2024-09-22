
# # Connect to the OpenHardwareMonitor WMI namespace
# w = wmi.WMI(namespace="root\OpenHardwareMonitor")

# # Access temperature sensors
# temperature_infos = w.Sensor()

# # Iterate through all sensors to find and print temperature data
# for sensor in temperature_infos:
#     if sensor.SensorType == 'Temperature':
#         print(f"Sensor Name: {sensor.Name}")
#         print(f"Sensor Value: {sensor.Value}°C")
#         print()
