// Content script for AI Month Dashboard Extension

console.log('AI Month Dashboard Extension content script loaded');

// This content script can be used to inject functionality into web pages
// For now, it just logs that it's loaded

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'new_announcement') {
        // Could inject announcement into the current page
        console.log('New announcement received in content script:', message.data);
    }
}); 