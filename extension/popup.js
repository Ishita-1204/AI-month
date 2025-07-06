// API base URL
const API_BASE = 'http://localhost:5000';

// DOM elements
const authSection = document.getElementById('authSection');
const userSection = document.getElementById('userSection');
const announcementsModal = document.getElementById('announcementsModal');
const announcementsBar = document.getElementById('announcementsBar');
const closeAnnouncementsModal = document.getElementById('closeAnnouncementsModal');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const announcementsList = document.getElementById('announcementsList');
const maximizeBtn = document.getElementById('maximizeBtn');
const minimizeBtn = document.getElementById('minimizeBtn');

// State
let isMaximized = false;
let todaysTasks = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    setupEventListeners();
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
    
    // Announcements bar click
    if (announcementsBar) {
        announcementsBar.addEventListener('click', function() {
            showAnnouncementsModal();
        });
    }
    // Modal close button
    if (closeAnnouncementsModal) {
        closeAnnouncementsModal.addEventListener('click', function() {
            hideAnnouncementsModal();
        });
    }
    // Modal overlay click (outside content)
    if (announcementsModal) {
        announcementsModal.addEventListener('click', function(e) {
            if (e.target === announcementsModal) {
                hideAnnouncementsModal();
            }
        });
    }
    
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
                loadTodaysTasks();
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

// Show user dashboard section
function showUserSection(username) {
    authSection.classList.add('hidden');
    userSection.classList.remove('hidden');
    document.getElementById('welcomeText').textContent = `Welcome, ${username}!`;
    
    // Show welcome banner
    const welcomeBanner = document.getElementById('welcomeBanner');
    const welcomeMessage = document.getElementById('welcomeMessage');
    if (welcomeBanner && welcomeMessage) {
        welcomeMessage.textContent = `Hello, ${username}! Welcome to AI Month!`;
        welcomeBanner.style.display = 'block';
    }
}

// Show announcements section
function showAnnouncementsModal() {
    if (announcementsModal) {
        announcementsModal.style.display = 'flex';
        loadTodaysTasks();
    }
}

function hideAnnouncementsModal() {
    if (announcementsModal) {
        announcementsModal.style.display = 'none';
    }
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
            
            // Show user section and load tasks
            showUserSection(username);
            clearErrors();
            await loadTodaysTasks();
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
            // Show success message briefly, then switch to login
            showSuccess('signupError', 'Account created successfully! You can now sign in.');
            setTimeout(() => {
                showLogin();
                clearErrors();
            }, 2000);
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
    todaysTasks = [];
    renderTasks();
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

// Load today's tasks
async function loadTodaysTasks() {
    try {
        console.log('Loading today\'s tasks...');
        const response = await fetch(`${API_BASE}/api/todays-announcements`);
        console.log('Response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('Tasks data:', data);
            
            if (data.announcements && Array.isArray(data.announcements)) {
                todaysTasks = data.announcements.map(task => ({
                    title: task.title,
                    description: task.body,
                    created_at: task.created_at,
                    created_by: task.created_by
                }));
                console.log('Processed tasks:', todaysTasks);
                renderTasks();
            } else {
                console.log('No tasks array in response:', data);
                todaysTasks = [];
                renderTasks();
            }
        } else {
            console.error('Failed to load tasks:', response.status, response.statusText);
            todaysTasks = [];
            renderTasks();
        }
    } catch (error) {
        console.error('Error loading today\'s tasks:', error);
        todaysTasks = [];
        renderTasks();
    }
}

// Render tasks
function renderTasks() {
    if (todaysTasks.length === 0) {
        announcementsList.innerHTML = '<div class="no-tasks">No announcements for today yet! Check back later for updates.</div>';
        return;
    }
    
    announcementsList.innerHTML = todaysTasks.map(task => {
        const time = new Date(task.created_at).toLocaleTimeString();
        return `
            <div class="task-card">
                <div class="task-title">${task.title}</div>
                <div class="task-description">${task.description}</div>
                <div class="task-time">Posted at ${time}</div>
            </div>
        `;
    }).join('');
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
    if (message.type === 'new_task') {
        loadTodaysTasks();
        showNotification('New task added!');
    }
});

// On popup open, always load latest tasks if logged in
window.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (token) {
        await loadTodaysTasks();
    }
}); 