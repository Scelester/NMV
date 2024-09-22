let lastBytesSent = 0;
let lastBytesRecv = 0;

function updateNetworkTraffic() {
  fetch('/network-traffic/')
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('bytesSent').innerText = (data.bytes_sent / 1_000_000).toFixed(2) + ' MB';
      document.getElementById('bytesRecv').innerText = (data.bytes_recv / 1_000_000).toFixed(2) + ' MB';

      const bytesSentDiff = lastBytesSent === 0 ? 0 : data.bytes_sent - lastBytesSent;
      const bytesRecvDiff = lastBytesRecv === 0 ? 0 : data.bytes_recv - lastBytesRecv;

      lastBytesSent = data.bytes_sent;
      lastBytesRecv = data.bytes_recv;

      updateChart(bytesSentDiff, bytesRecvDiff);
    })
    .catch((error) => console.error('Error:', error));
}

const ctx = document.getElementById('bandwidthChart').getContext('2d');
const bandwidthChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Data Sent (MB)',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderWidth: 1,
        fill: true,
      },
      {
        label: 'Data Received (MB)',
        data: [],
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderWidth: 1,
        fill: true,
      }
    ]
  },
  options: {
    responsive: false,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'second',
        },
        title: {
          display: true,
          text: 'Time'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Data (MB)'
        }
      }
    }
  }
});

function updateChart(sentDiff, recvDiff) {
  const now = new Date();

  bandwidthChart.data.labels.push(now);
  bandwidthChart.data.datasets[0].data.push(sentDiff / 1_000_000); // Convert bytes to MB
  bandwidthChart.data.datasets[1].data.push(recvDiff / 1_000_000); // Convert bytes to MB

  // Keep the chart data length within limits (e.g., 60 data points)
  if (bandwidthChart.data.labels.length > 60) {
    bandwidthChart.data.labels.shift();
    bandwidthChart.data.datasets[0].data.shift();
    bandwidthChart.data.datasets[1].data.shift();
  }

  bandwidthChart.update();
}
