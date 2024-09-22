function updateDeviceStatus() {
    fetch('/device-availability/')
        .then((response) => response.json())
        .then((data) => {
            const statusList = document.getElementById('statusList');
            statusList.innerHTML = '';
            for (const [name, info] of Object.entries(data)) {
                const listItem = document.createElement('li');
                
                const deviceName = document.createElement('span');
                deviceName.className = 'device-name';
                deviceName.innerText = name;
                
                const deviceInfo = document.createElement('span');
                deviceInfo.className = 'device-info';
                deviceInfo.innerHTML = `
                    Online: <span class="${info.online ? 'online' : 'offline'}">${info.online ? 'Yes' : 'No'}</span>, 
                    Packet Loss: ${info.packet_loss}%, 
                    Ping Time: ${info.ping_time !== 'N/A' ? info.ping_time.toFixed(2) + ' ms' : 'N/A'}
                `;

                listItem.appendChild(deviceName);
                listItem.appendChild(deviceInfo);
                statusList.appendChild(listItem);
            }
        })
        .catch((error) => console.error('Error:', error));
}

// Call the function to update the device status when the page loads
document.addEventListener('DOMContentLoaded', updateDeviceStatus);
