# AI Month Dashboard - Deployment Guide

This guide will help you deploy the AI Month Dashboard to various platforms.

## 🚀 Quick Deployment

### 1. Local Development
```bash
# Clone the repository
git clone <your-repo-url>
cd AI-month-dashboard

# Run setup
python setup.py

# Start the application
python start.py
```

### 2. Production Deployment

#### Prerequisites
- Python 3.8+
- PostgreSQL
- Web server (Nginx/Apache)
- Domain name (optional)

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y
```

#### Step 2: Application Setup
```bash
# Clone repository
git clone <your-repo-url>
cd AI-month-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn
```

#### Step 3: Database Setup
```bash
# Access PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE signin_app;
CREATE USER dashboard_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE signin_app TO dashboard_user;
\q
```

#### Step 4: Application Configuration
```bash
# Create environment file
cat > .env << EOF
DATABASE_URL=postgresql://dashboard_user:your_password@localhost/signin_app
SECRET_KEY=your-secret-key-here
DEBUG=False
SOCKET_PORT=8080
EOF
```

#### Step 5: Gunicorn Configuration
```bash
# Create Gunicorn service file
sudo tee /etc/systemd/system/ai-dashboard.service << EOF
[Unit]
Description=AI Month Dashboard
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/AI-month-dashboard
Environment="PATH=/path/to/AI-month-dashboard/venv/bin"
ExecStart=/path/to/AI-month-dashboard/venv/bin/gunicorn --workers 3 --bind unix:ai-dashboard.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
EOF

# Start and enable service
sudo systemctl start ai-dashboard
sudo systemctl enable ai-dashboard
```

#### Step 6: Nginx Configuration
```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/ai-dashboard << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/AI-month-dashboard/ai-dashboard.sock;
    }

    location /socket.io/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/ai-dashboard /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 🌐 Cloud Deployment

### Heroku Deployment

#### Step 1: Prepare for Heroku
```bash
# Create Procfile
echo "web: gunicorn main:app" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Update requirements.txt
echo "gunicorn" >> requirements.txt
```

#### Step 2: Deploy to Heroku
```bash
# Install Heroku CLI
# Follow instructions at: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

### Docker Deployment

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000 8080

CMD ["python", "main.py"]
```

#### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/signin_app
      - SECRET_KEY=your-secret-key
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=signin_app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Step 3: Deploy with Docker
```bash
# Build and run
docker-compose up --build

# Or run in background
docker-compose up -d
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost/signin_app` |
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `True` |
| `SOCKET_PORT` | WebSocket port | `8080` |
| `HOST` | Host address | `0.0.0.0` |
| `PORT` | Main port | `5000` |

## 🔒 Security Considerations

### Production Security
1. **Use HTTPS**: Always use SSL/TLS in production
2. **Strong Secret Key**: Generate a strong secret key
3. **Database Security**: Use strong database passwords
4. **Environment Variables**: Never commit secrets to Git
5. **Firewall**: Configure firewall rules
6. **Regular Updates**: Keep dependencies updated

### Security Checklist
- [ ] HTTPS enabled
- [ ] Strong secret key set
- [ ] Database password changed
- [ ] Debug mode disabled
- [ ] Environment variables configured
- [ ] Firewall configured
- [ ] Dependencies updated

## 📊 Monitoring

### Log Monitoring
```bash
# View application logs
sudo journalctl -u ai-dashboard -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks
```bash
# Check application status
curl http://localhost:5000/api/verify

# Check WebSocket
curl http://localhost:8080/socket.io/
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connection
psql -h localhost -U dashboard_user -d signin_app
```

#### 2. Port Already in Use
```bash
# Find process using port
sudo netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R www-data:www-data /path/to/AI-month-dashboard
sudo chmod -R 755 /path/to/AI-month-dashboard
```

## 📈 Performance Optimization

### Gunicorn Configuration
```bash
# Optimize workers
gunicorn --workers 4 --worker-class gevent --bind 0.0.0.0:5000 app:app
```

### Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_sessions_token ON sessions(token);
```

### Caching
```python
# Add Redis caching
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis'})
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# Create backup
pg_dump signin_app > backup_$(date +%Y%m%d).sql

# Restore backup
psql signin_app < backup_20231201.sql
```

### Application Backup
```bash
# Backup application files
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/AI-month-dashboard
```

---

**AI Month Dashboard** - Complete deployment guide for production environments. 