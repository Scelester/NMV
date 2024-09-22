function updateAppUsage() {
  fetch('/network-usage/')
    .then((response) => response.json())
    .then((data) => {
      const appUsageList = document.getElementById('appUsageList')
      appUsageList.innerHTML = ''
      data.forEach((app) => {
        const listItem = document.createElement('li')

        // Create a container for app name and data usage
        const appInfoContainer = document.createElement('div')
        appInfoContainer.className = 'app-info'

        // Create and set up the app name element
        const appNameElement = document.createElement('span')
        appNameElement.className = 'app-name'
        appNameElement.innerText = `App: ${app.app_name}`

        // Create and set up the data usage element
        const dataUsageElement = document.createElement('span')
        dataUsageElement.className = 'data-usage'
        dataUsageElement.innerText = `Data Usage: ${app.connections}`

        // Append elements to the container
        appInfoContainer.appendChild(appNameElement)
        appInfoContainer.appendChild(dataUsageElement)

        // Append the container to the list item
        listItem.appendChild(appInfoContainer)

        // Append the list item to the list
        appUsageList.appendChild(listItem)
      })
    })
    .catch((error) => console.error('Error:', error))
}
