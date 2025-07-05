// Background script for AI Month Dashboard Extension

// WebSocket connection
let socket = null;
let isConnected = false;

// Initialize when extension loads
chrome.runtime.onInstalled.addListener(() => {
    console.log('AI Month Dashboard Extension installed');
    connectWebSocket();
});

// Connect to WebSocket server
function connectWebSocket() {
    try {
        socket = new WebSocket('ws://localhost:5000/socket.io/?EIO=4&transport=websocket');
        
        socket.onopen = function() {
            console.log('WebSocket connected');
            isConnected = true;
        };
        
        socket.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'new_announcement') {
                    handleNewAnnouncement(data.data);
                }
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };
        
        socket.onclose = function() {
            console.log('WebSocket disconnected');
            isConnected = false;
            // Reconnect after 5 seconds
            setTimeout(connectWebSocket, 5000);
        };
        
        socket.onerror = function(error) {
            console.error('WebSocket error:', error);
            isConnected = false;
        };
        
    } catch (error) {
        console.error('Failed to connect to WebSocket:', error);
        // Retry connection after 10 seconds
        setTimeout(connectWebSocket, 10000);
    }
}

// Handle new announcement
function handleNewAnnouncement(announcement) {
    console.log('New announcement received:', announcement);
    
    // Send to popup if open
    chrome.runtime.sendMessage({
        type: 'new_announcement',
        data: announcement
    });
    
    // Show browser notification
    showNotification(announcement);
}

// Show browser notification
function showNotification(announcement) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'AI Month Dashboard',
        message: announcement.title,
        contextMessage: announcement.body.replace(/<[^>]*>/g, '').substring(0, 100) + '...'
    });
}

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
    // This will open the popup automatically due to manifest configuration
});

// Handle messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'connect_websocket') {
        connectWebSocket();
        sendResponse({ success: true });
    }
});

// Keep connection alive
setInterval(() => {
    if (!isConnected) {
        connectWebSocket();
    }
}, 30000); // Check every 30 seconds

// Handle extension startup
chrome.runtime.onStartup.addListener(() => {
    console.log('AI Month Dashboard Extension started');
    connectWebSocket();
}); 