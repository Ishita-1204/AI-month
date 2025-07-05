# AI Month Dashboard Browser Extension

A browser extension that provides a compact dashboard for the AI Month signin system with real-time announcements.

## Features

- 🔐 **Authentication**: Sign in, sign up, and sign out functionality
- 📢 **Real-time Announcements**: Receive notifications for new announcements
- 🎯 **Compact Dashboard**: Small popup that can be maximized
- 🔔 **Browser Notifications**: Get notified of new announcements even when the popup is closed
- 💾 **Persistent Storage**: Your announcements are saved locally

## Installation

### Prerequisites
- Make sure the AI Month Flask app is running on `http://localhost:5000`
- Chrome, Firefox, or Edge browser

### Steps to Install

1. **Download/Clone the extension folder**
   ```
   extension/
   ├── manifest.json
   ├── popup.html
   ├── popup.js
   ├── background.js
   ├── content.js
   ├── icons/
   │   ├── icon16.png
   │   ├── icon48.png
   │   └── icon128.png
   └── README.md
   ```

2. **Create Icon Files**
   - Create 16x16, 48x48, and 128x128 PNG icons
   - Place them in the `icons/` folder
   - Or use any existing icons with these dimensions

3. **Load Extension in Chrome**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `extension/` folder

4. **Load Extension in Firefox**
   - Open Firefox and go to `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Select the `manifest.json` file

## Usage

### Basic Usage
1. **Click the extension icon** in your browser toolbar
2. **Sign in** with your AI Month credentials:
   - Username: `alice`, Password: `password1`
   - Username: `bob`, Password: `password2`
   - Or create a new account using signup
3. **View announcements** in the dashboard
4. **Maximize** the popup for a larger view

### Features
- **Compact Mode**: Default small popup (350px width)
- **Maximized Mode**: Larger view (600px width) - click the ⛶ button
- **Real-time Updates**: Announcements appear automatically
- **Browser Notifications**: Get notified even when popup is closed
- **Persistent Login**: Stay logged in between browser sessions

### Announcements
- Welcome announcements when you sign in/sign up
- Real-time announcements from the server
- Browser notifications for new announcements
- Local storage of recent announcements

## Development

### File Structure
```
extension/
├── manifest.json          # Extension configuration
├── popup.html            # Main popup interface
├── popup.js              # Popup functionality
├── background.js         # Background service worker
├── content.js            # Content script (injected into pages)
└── icons/                # Extension icons
```

### API Endpoints Used
- `POST /api/signin` - User authentication
- `POST /api/signup` - User registration
- `POST /api/signout` - User logout
- `GET /api/verify` - Token verification
- WebSocket connection for real-time announcements

### Customization
- Modify `popup.html` for UI changes
- Update `popup.js` for functionality changes
- Edit `background.js` for WebSocket handling
- Change colors and styling in the CSS

## Troubleshooting

### Common Issues

1. **Extension won't load**
   - Check that all files are in the correct location
   - Ensure `manifest.json` is valid JSON
   - Verify icon files exist and are PNG format

2. **Can't connect to server**
   - Make sure the Flask app is running on `http://localhost:5000`
   - Check that the server is accessible
   - Verify CORS settings in the Flask app

3. **WebSocket connection fails**
   - The extension will automatically retry connections
   - Check browser console for error messages
   - Ensure the Flask app supports WebSocket connections

4. **Notifications not working**
   - Check browser notification permissions
   - Click "Allow" when prompted for notification access
   - Verify the extension has notification permissions

### Debug Mode
- Open browser developer tools
- Check the Console tab for error messages
- Look for messages from the extension background script
- Verify network requests in the Network tab

## Security Notes

- The extension stores authentication tokens in browser storage
- Tokens are automatically verified on each popup open
- Invalid tokens are cleared automatically
- All API communication uses HTTPS (in production)

## Future Enhancements

- [ ] Add more announcement types
- [ ] Implement announcement categories
- [ ] Add user preferences
- [ ] Create announcement history
- [ ] Add offline support
- [ ] Implement push notifications 