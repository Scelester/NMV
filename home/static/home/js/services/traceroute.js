function updateTraceroute() {
  const host = document.getElementById('tracerouteHost').value;
  const spinner = document.getElementById('spinner');
  const tracerouteList = document.getElementById('tracerouteList');

  // Show the spinner
  spinner.style.display = 'block';
  tracerouteList.innerHTML = '';

  fetch(`/trace-route/?host=${encodeURIComponent(host)}`)
      .then((response) => response.json())
      .then((data) => {
          tracerouteList.innerHTML = '';
          data.forEach((hop) => {
              const listItem = document.createElement('li');
              listItem.classList.add('hop');
  
              // Create header for hop
              const hopHeader = document.createElement('div');
              hopHeader.classList.add('hop-header');
  
              // Add icon
              const icon = document.createElement('img');
              icon.src = '/static/home/img/router.png'; // Path to your icon
              icon.alt = 'Router Icon';
              icon.classList.add('hop-icon');
  
              // Add hop details
              const hopDetails = document.createElement('div');
              hopDetails.classList.add('hop-details');
              const latencies = hop.latencies
                  .map((latency) => (latency.trim() ? `<span class="latency">${latency} ms</span>` : ''))
                  .filter((latency) => latency !== '') // Remove empty latency entries
                  .join(' '); // Use space instead of commas
  
              hopDetails.innerHTML = `Hop ${hop.hop}: <strong>${hop.hostname}</strong> (${hop.address}) - ${latencies}`;
  
              // Append icon and details to header
              hopHeader.appendChild(icon);
              hopHeader.appendChild(hopDetails);
  
              // Append header to list item
              listItem.appendChild(hopHeader);
              tracerouteList.appendChild(listItem);
          });
      })
      .catch((error) => console.error('Error:', error))
      .finally(() => {
          // Hide the spinner after data is loaded
          spinner.style.display = 'none';
      });
}
