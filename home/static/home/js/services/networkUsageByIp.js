function updateNetworkUsage() {
  fetch('/network-usage-by-ip/')
    .then((response) => response.json())
    .then((data) => {
      const networkUsageList = document.getElementById('networkUsageList')
      networkUsageList.innerHTML = ''
      data.forEach(([ip, usage]) => {
        const listItem = document.createElement('li')
        
        // Create elements for IP and usage
        const ipElement = document.createElement('span')
        ipElement.className = 'ip'
        ipElement.innerText = `IP: ${ip}`
        
        const usageElement = document.createElement('span')
        usageElement.className = 'usage'
        usageElement.innerText = `Data Usage: ${usage}`
        
        // Append elements to the list item
        listItem.appendChild(ipElement)
        listItem.appendChild(usageElement)
        
        // Append the list item to the list
        networkUsageList.appendChild(listItem)
      })
    })
    .catch((error) => console.error('Error:', error))
}
