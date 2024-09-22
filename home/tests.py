import psutil

def system_usage_data():
    cpu_load = psutil.cpu_percent(interval=1)
    if cpu_load <= 90:
        cpu_load = cpu_load * 10
        
    memory = psutil.virtual_memory()
    memory_used = memory.used / (1024 ** 3)  # Convert to GB
    memory_total = memory.total / (1024 ** 3)  # Convert to GB
    memory_percent = memory.percent

    data = {
        'cpu_load': cpu_load,
        'memory_used': round(memory_used, 2),
        'memory_total': round(memory_total, 2),
        'memory_percent': memory_percent,
    }

    return data

print(system_usage_data())