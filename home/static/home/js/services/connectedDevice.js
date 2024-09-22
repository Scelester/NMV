function updateConnectedDevices() {
    const dotsContainer = document.getElementById('dotsContainer');
    const devicesList = document.getElementById('devicesList');

    // Show the fading dots
    dotsContainer.style.display = 'flex';
    devicesList.innerHTML = '';

    fetch('/connected-devices/')
        .then((response) => response.json())
        .then((data) => {
            devicesList.innerHTML = '';
            data.forEach((device, index) => {
                const listItem = document.createElement('li');
                
                // Create a container for the image and text
                const deviceContainer = document.createElement('div');
                deviceContainer.className = 'device-container';
                
                // Create and set up the image element
                const deviceImage = document.createElement('img');
                deviceImage.src = '/static/home/img/device.png'; // Static image URL
                deviceImage.alt = 'Device Image';
                deviceImage.className = 'device-image';

                // Create and set up the text element
                const deviceText = document.createElement('span');
                deviceText.innerText = `Device ${index + 1} - IP: ${device.ip}`;
                deviceText.className = 'device-text';

                // Append the image and text to the container
                deviceContainer.appendChild(deviceImage);
                deviceContainer.appendChild(deviceText);
                
                // Append the container to the list item
                listItem.appendChild(deviceContainer);
                
                // Append the list item to the devices list
                devicesList.appendChild(listItem);
            });
        })
        .catch((error) => console.error('Error:', error))
        .finally(() => {
            // Hide the fading dots after data is loaded
            dotsContainer.style.display = 'none';
        });
}

// Attach the click event to the refresh button
document.getElementById('refreshDevices').addEventListener('click', updateConnectedDevices);

// Optionally, you can call the function once on page load to show data immediately
document.addEventListener('DOMContentLoaded', updateConnectedDevices);
