// Request notification permission from the user
function requestNotificationPermission() {
    if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            if (permission !== 'granted') {
                console.log('Notification permission denied.');
            }
        });
    }
}

function sendDesktopNotification(subject, message) {
    if (Notification.permission === 'granted') {
        new Notification(subject, {
            body: message,
            icon: `${window.location.origin}/static/home/favicon.png`, 
        });
    }
}

function fetchNotifications() {
    fetch('/notifications/')
        .then(response => response.json())
        .then(notifications => {
            notifications.forEach(notification => {
                sendDesktopNotification(notification.subject, notification.message);
            });
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

// Request notification permission on page load
requestNotificationPermission();

// Check for notifications every 5 seconds
setInterval(fetchNotifications, 5000);

// Initial fetch
fetchNotifications();