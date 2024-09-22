let cpuGauge, memoryGauge;

function createGauges() {
  cpuGauge = new JustGage({
    id: 'cpuGauge',
    value: 0,
    min: 0,
    max: 100,
    title: 'CPU Load',
    label: 'Percentage',
    gaugeWidthScale: 0.6,
    levelColors: ['#00ff00', '#ffdd00', '#ff0000']
  });

  memoryGauge = new JustGage({
    id: 'memoryGauge',
    value: 0,
    min: 0,
    max: 100,
    title: 'Memory Usage',
    label: 'Percentage',
    gaugeWidthScale: 0.6,
    levelColors: ['#00ff00', '#ffdd00', '#ff0000']
  });
}

function updateSystemUsage() {
  fetch('/api/system-usage/')
    .then(response => response.json())
    .then(data => {
      cpuGauge.refresh(data.cpu_load);
      memoryGauge.refresh(data.memory_percent);
    })
    .catch(error => console.error('Error fetching system usage:', error));
}

createGauges();
setInterval(updateSystemUsage, 1000);
updateSystemUsage();  // Initial call to populate the data
