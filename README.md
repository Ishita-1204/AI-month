# AI Month Dashboard

A comprehensive real-time dashboard system with user authentication, announcements, and browser extension integration.

## 🚀 Features

- **User Authentication**: Sign up, sign in, and sign out functionality
- **Real-time Announcements**: WebSocket-based live announcements
- **Browser Extension**: Chrome/Firefox extension with dashboard and notifications
- **PostgreSQL Database**: Persistent storage for users and sessions
- **Responsive Design**: Modern UI with orange and white theme
- **Session Management**: Secure token-based authentication

## 📁 Project Structure

```
AI-month-dashboard/
├── backend/                 # Flask backend API
│   ├── api.py              # API endpoints
│   ├── models.py           # Database models
│   ├── app.py              # Flask app configuration
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Web frontend
│   ├── templates/          # HTML templates
│   └── static/            # CSS and JavaScript
├── extension/              # Browser extension
│   ├── popup.html         # Extension popup UI
│   ├── popup.js           # Extension logic
│   ├── background.js      # Background service worker
│   ├── content.js         # Content script
│   ├── manifest.json      # Extension manifest
│   └── icons/            # Extension icons
├── docs/                  # Documentation
│   ├── README.md         # Main documentation
│   ├── postgresql_setup.md
│   ├── pgadmin_guide.md
│   └── extension_guide.md
├── main.py                # Main Flask application
├── requirements.txt       # Python dependencies
└── .gitignore           # Git ignore file
```

## 🛠️ Quick Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Modern web browser (Chrome/Firefox)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AI-month-dashboard
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL**
   - Install PostgreSQL
   - Create a database named `signin_app`
   - Update database connection in `main.py` if needed

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   - Web App: http://localhost:5000
   - Announcements: http://localhost:8080

## 🔧 Configuration

### Database Configuration

The app uses PostgreSQL by default. Update the database URL in `main.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/signin_app'
```

### Extension Setup

1. Open Chrome/Firefox
2. Go to Extensions (chrome://extensions or about:addons)
3. Enable Developer Mode
4. Load unpacked extension from `extension/` folder

## 📊 API Endpoints

- `POST /api/signup` - User registration
- `POST /api/signin` - User login
- `POST /api/signout` - User logout
- `GET /api/verify` - Verify session token
- `GET /socket.io/` - WebSocket for real-time announcements

## 🎨 Features

### Web Application
- User authentication with session management
- Real-time announcements via WebSocket
- Responsive design with modern UI
- Personalized welcome messages

### Browser Extension
- Dashboard with sign in/up functionality
- Real-time announcement notifications
- Persistent login state
- Orange and white theme

### Database
- PostgreSQL with SQLAlchemy ORM
- User and session management
- Automatic database creation

## 🔍 Database Queries

To view users in pgAdmin:
```sql
SELECT id, username, password, created_at 
FROM users 
ORDER BY created_at DESC;
```

## 📚 Documentation

- [PostgreSQL Setup Guide](docs/postgresql_setup.md)
- [pgAdmin Database Guide](docs/pgadmin_guide.md)
- [Extension Installation Guide](docs/extension_guide.md)

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production
- Use a production WSGI server like Gunicorn
- Configure environment variables for database
- Set up proper SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
- Check the documentation in `docs/`
- Review the database setup guides
- Test the extension installation

---

**AI Month Dashboard** - Real-time authentication and announcement system with browser extension integration. 