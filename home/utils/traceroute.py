import subprocess
import re

def perform_traceroute(target):
    try:
        result = subprocess.run(['tracert', target], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        hops = []

        # Updated regex pattern to match more lines
        pattern = re.compile(
            r'^\s*(\d+)\s+((?:\d+ ms\s+|\*\s*)+)([^\[]+)?(\[([^\]]+)\])?',
            re.IGNORECASE
        )

        for line in lines:
            match = pattern.match(line)
            if match:
                hop_num = int(match.group(1))
                latencies = match.group(2).strip().split()
                hostname = match.group(3).strip() if match.group(3) else "N/A"
                ip_address = match.group(5).strip() if match.group(5) else "N/A"

                # Clean up the latencies to remove 'ms' and '*' and ensure they are in milliseconds
                latencies = [latency.replace('ms', '').strip() for latency in latencies if latency != '*']

                icon = 'router-icon.png' if 'router' in hostname.lower() else 'device-icon.png'

                hops.append({
                    'hop': hop_num,
                    'hostname': hostname,
                    'address': ip_address,
                    'latencies': latencies,
                    'icon': icon
                })

        return hops
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
