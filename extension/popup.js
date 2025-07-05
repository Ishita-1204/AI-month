// API base URL
const API_BASE = 'http://localhost:5000';

// DOM elements
const authSection = document.getElementById('authSection');
const userSection = document.getElementById('userSection');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const announcementsList = document.getElementById('announcementsList');
const maximizeBtn = document.getElementById('maximizeBtn');
const minimizeBtn = document.getElementById('minimizeBtn');

// State
let isMaximized = false;
let announcements = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    setupEventListeners();
    loadAnnouncements();
});

// Setup event listeners
function setupEventListeners() {
    // Login
    document.getElementById('loginBtn').addEventListener('click', handleLogin);
    document.getElementById('showSignupBtn').addEventListener('click', showSignup);
    
    // Signup
    document.getElementById('signupBtn').addEventListener('click', handleSignup);
    document.getElementById('showLoginBtn').addEventListener('click', showLogin);
    
    // Logout
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    
    // Maximize/Minimize
    maximizeBtn.addEventListener('click', maximize);
    minimizeBtn.addEventListener('click', minimize);
    
    // Enter key handlers
    document.getElementById('username').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLogin();
    });
    document.getElementById('password').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLogin();
    });
    document.getElementById('signupUsername').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSignup();
    });
    document.getElementById('signupPassword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSignup();
    });
}

// Check authentication status
async function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    
    if (token && username) {
        // Verify token is still valid
        try {
            const response = await fetch(`${API_BASE}/api/verify`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                // User is already signed in, show user section directly
                showUserSection(username);
                fetchAnnouncementsFromBackend();
                return;
            }
        } catch (error) {
            console.error('Token verification failed:', error);
        }
    }
    
    // Only show auth section if user is not signed in
    showAuthSection();
}

// Show authentication section
function showAuthSection() {
    authSection.classList.remove('hidden');
    userSection.classList.add('hidden');
    clearErrors();
}

// Show user section
function showUserSection(username) {
    authSection.classList.add('hidden');
    userSection.classList.remove('hidden');
    document.getElementById('welcomeText').textContent = `Welcome, ${username}!`;
    
    // Load announcements when user section is shown
    fetchAnnouncementsFromBackend();
}

// Handle login
async function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showError('loginError', 'Please enter both username and password');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/signin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('username', username);
            
            // Store announcement if present
            if (data.announcement) {
                addAnnouncement(data.announcement);
                showNotification('Welcome! You have a new announcement!');
            }
            
            // Immediately show user section and load announcements
            showUserSection(username);
            clearErrors();
            await fetchAnnouncementsFromBackend();
        } else {
            showError('loginError', data.error || 'Login failed');
        }
    } catch (error) {
        showError('loginError', 'Connection error. Please try again.');
    }
}

// Handle signup
async function handleSignup() {
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;
    
    if (!username || !password) {
        showError('signupError', 'Please enter both username and password');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store announcement if present
            if (data.announcement) {
                addAnnouncement(data.announcement);
                showNotification('Account created! You have a new announcement!');
            }
            
            // Show success message briefly, then switch to login
            showSuccess('signupError', 'Account created successfully! You can now sign in.');
            setTimeout(() => {
                showLogin();
                clearErrors();
            }, 2000);
            await fetchAnnouncementsFromBackend();
        } else {
            showError('signupError', data.error || 'Signup failed');
        }
    } catch (error) {
        showError('signupError', 'Connection error. Please try again.');
    }
}

// Handle logout
async function handleLogout() {
    const token = localStorage.getItem('token');
    
    try {
        await fetch(`${API_BASE}/api/signout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    showAuthSection();
    announcements = [];
    renderAnnouncements();
}

// Show signup form
function showSignup() {
    loginForm.classList.add('hidden');
    signupForm.classList.remove('hidden');
    clearErrors();
}

// Show login form
function showLogin() {
    signupForm.classList.add('hidden');
    loginForm.classList.remove('hidden');
    clearErrors();
}

// Maximize popup
function maximize() {
    document.body.classList.add('maximized');
    maximizeBtn.style.display = 'none';
    minimizeBtn.style.display = 'block';
    isMaximized = true;
}

// Minimize popup
function minimize() {
    document.body.classList.remove('maximized');
    minimizeBtn.style.display = 'none';
    maximizeBtn.style.display = 'block';
    isMaximized = false;
}

// Show error message
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.classList.remove('hidden');
}

// Show success message
function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.classList.remove('hidden');
    element.classList.add('success');
}

// Clear all errors
function clearErrors() {
    document.querySelectorAll('.error').forEach(el => {
        el.classList.add('hidden');
        el.classList.remove('success');
    });
}

// Add announcement
function addAnnouncement(announcement) {
    announcements.unshift(announcement);
    if (announcements.length > 5) {
        announcements = announcements.slice(0, 5);
    }
    renderAnnouncements();
}

// Render announcements
function renderAnnouncements() {
    if (announcements.length === 0) {
        announcementsList.innerHTML = '<div class="loading">No announcements yet. Sign in to see updates!</div>';
        return;
    }
    
    announcementsList.innerHTML = announcements.map(announcement => {
        const time = new Date(announcement.timestamp * 1000).toLocaleTimeString();
        return `
            <div class="announcement">
                <div class="announcement-title">${announcement.title}</div>
                <div class="announcement-body">${announcement.body}</div>
                <div class="announcement-time">${time}</div>
            </div>
        `;
    }).join('');
}

// Load announcements from storage
function loadAnnouncements() {
    const stored = localStorage.getItem('announcements');
    if (stored) {
        try {
            announcements = JSON.parse(stored);
            renderAnnouncements();
        } catch (error) {
            console.error('Error loading announcements:', error);
        }
    }
}

// Save announcements to storage
function saveAnnouncements() {
    localStorage.setItem('announcements', JSON.stringify(announcements));
}

// Show browser notification
function showNotification(message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('AI Month Dashboard', {
            body: message,
            icon: 'icons/icon48.png'
        });
    }
}

// Request notification permission
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'new_announcement') {
        addAnnouncement(message.data);
        showNotification('New announcement received!');
    }
});

// Save announcements when they change
const originalAddAnnouncement = addAnnouncement;
addAnnouncement = function(announcement) {
    originalAddAnnouncement(announcement);
    saveAnnouncements();
};

// Fetch announcements from backend
async function fetchAnnouncementsFromBackend() {
    try {
        console.log('Fetching announcements from backend...');
        const response = await fetch(`${API_BASE}/api/announcements`);
        console.log('Response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('Announcements data:', data);
            
            if (data.announcements && Array.isArray(data.announcements)) {
                announcements = data.announcements.map(a => ({
                    title: a.title,
                    body: a.body,
                    timestamp: a.timestamp || (new Date(a.created_at).getTime() / 1000),
                    created_by: a.created_by
                }));
                console.log('Processed announcements:', announcements);
                saveAnnouncements();
                renderAnnouncements();
            } else {
                console.log('No announcements array in response:', data);
                announcements = [];
                renderAnnouncements();
            }
        } else {
            console.error('Failed to fetch announcements:', response.status, response.statusText);
            announcements = [];
            renderAnnouncements();
        }
    } catch (error) {
        console.error('Error fetching announcements:', error);
        announcements = [];
        renderAnnouncements();
    }
}

// On popup open, always fetch latest announcements if logged in
window.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (token) {
        await fetchAnnouncementsFromBackend();
    } else {
        loadAnnouncements();
    }
}); 