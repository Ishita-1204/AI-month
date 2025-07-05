# Real-time Announcement System

A standalone real-time announcement system built with Flask and Socket.IO that allows instant broadcasting of announcements to all connected clients.

## 🚀 Features

- **Real-time Updates**: Instant announcement delivery via WebSocket
- **Modern UI**: Clean, responsive design with smooth animations
- **Connection Status**: Live connection indicator
- **RESTful API**: Simple POST endpoint for sending announcements
- **Auto-cleanup**: Keeps only the last 10 announcements

## 📁 Project Structure

```
announcement-system/
├── backend/
│   ├── app.py              # Flask server with Socket.IO
│   └── requirements.txt     # Python dependencies
└── frontend/
    └── index.html          # Main frontend page
```

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
cd backend
python app.py
```

### 3. Access the Application

Open your browser and go to: **http://localhost:8080**

## 🧪 Testing the System

### Using curl

```bash
# Send a test announcement
curl -X POST http://localhost:8080/api/announce \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Announcement", "body": "This is a test announcement!"}'

# Send another announcement
curl -X POST http://localhost:8080/api/announce \
  -H "Content-Type: application/json" \
  -d '{"title": "Important Update", "body": "System maintenance scheduled for tonight at 2 AM."}'
```

### Using Postman

1. **Method**: POST
2. **URL**: `http://localhost:8080/api/announce`
3. **Headers**: `Content-Type: application/json`
4. **Body** (raw JSON):
   ```json
   {
     "title": "Your Title",
     "body": "Your announcement message"
   }
   ```

## 🔧 API Reference

### POST `/api/announce`

Sends a new announcement to all connected clients.

**Request Body:**
```json
{
  "title": "Announcement Title",
  "body": "Announcement message content"
}
```

**Response:**
```json
{
  "message": "Announcement sent successfully",
  "title": "Announcement Title",
  "body": "Announcement message content"
}
```

## 🎯 How It Works

1. **Frontend**: Connects to Socket.IO server and listens for `new_announcement` events
2. **API Call**: POST request to `/api/announce` with title and body
3. **Server Processing**: Validates data and emits Socket.IO event
4. **Real-time Delivery**: All connected clients receive the announcement instantly
5. **UI Update**: Frontend displays the announcement with smooth animation

## 🔌 WebSocket Events

- **`new_announcement`**: Emitted when a new announcement is sent
  - Data: `{title, body, timestamp}`

## 🎨 Frontend Features

- **Connection Status**: Visual indicator showing WebSocket connection state
- **Responsive Design**: Works on desktop and mobile devices
- **Smooth Animations**: Cards slide in with CSS animations
- **Auto-cleanup**: Maintains only the last 10 announcements
- **Timestamp Display**: Shows when each announcement was received

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
For production deployment, consider using:
- **Gunicorn** with eventlet worker
- **Nginx** as reverse proxy
- **Redis** for Socket.IO adapter (for multiple server instances)

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (default: 'your-secret-key-here')
- `PORT`: Server port (default: 8080)

### Customization
- Modify `frontend/index.html` for UI changes
- Update `backend/app.py` for backend logic
- Add database integration for persistent announcements

## 📱 Integration

This system is designed to be easily integrated into larger applications:

1. **Dashboard Integration**: Include the frontend in existing dashboards
2. **API Integration**: Use the `/api/announce` endpoint from other applications
3. **Database Integration**: Add persistent storage for announcements
4. **Authentication**: Add user authentication for announcement creation

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change port in `app.py` or kill existing process
2. **Socket.IO connection failed**: Check if server is running and firewall settings
3. **CORS issues**: Already configured for all origins in development

### Debug Mode
The server runs in debug mode by default. Check console for detailed logs.

## 📄 License

This project is open source and available under the MIT License. 