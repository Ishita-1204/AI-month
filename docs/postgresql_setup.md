# PostgreSQL Setup Guide

## Prerequisites

1. **Install PostgreSQL Server**:
   - Download from: https://www.postgresql.org/download/
   - Or use package manager:
     ```bash
     # Windows (using Chocolatey)
     choco install postgresql
     
     # macOS (using Homebrew)
     brew install postgresql
     
     # Ubuntu/Debian
     sudo apt-get install postgresql postgresql-contrib
     ```

2. **Install PostgreSQL Python Connector**:
   ```bash
   pip install psycopg2-binary
   ```

## PostgreSQL Setup Steps

### 1. Start PostgreSQL Service
```bash
# Windows
net start postgresql

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### 2. Access PostgreSQL Command Line
```bash
# Connect as postgres user
psql -U postgres

# Or on some systems
sudo -u postgres psql
```

### 3. Create Database and User
```sql
-- Create the database
CREATE DATABASE signin_app;

-- Create a dedicated user (recommended for security)
CREATE USER signin_user WITH PASSWORD 'your_secure_password';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE signin_app TO signin_user;

-- Connect to the signin_app database
\c signin_app

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO signin_user;

-- Exit PostgreSQL
\q
```

### 4. Update App Configuration

Edit `app.py` and update the database URI with your credentials:

```python
# Replace with your actual PostgreSQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://signin_user:your_secure_password@localhost/signin_app'
```

### 5. Run the Application
```bash
python app.py
```

## Troubleshooting

### Common Issues:

1. **Connection Error**: Make sure PostgreSQL is running
2. **Access Denied**: Check username/password in the URI
3. **Database Not Found**: Ensure the database was created
4. **Module Not Found**: Install psycopg2-binary: `pip install psycopg2-binary`

### Test Connection:
```python
import psycopg2
try:
    connection = psycopg2.connect(
        host='localhost',
        user='signin_user',
        password='your_secure_password',
        database='signin_app'
    )
    print("PostgreSQL connection successful!")
    connection.close()
except Exception as e:
    print(f"PostgreSQL connection failed: {e}")
```

## PostgreSQL vs MySQL Benefits

- **ACID Compliance**: Better transaction handling
- **JSON Support**: Native JSON data types
- **Advanced Features**: Full-text search, arrays, custom types
- **Performance**: Often faster for complex queries
- **Standards**: Better SQL standard compliance

## Security Notes

- Use strong passwords
- Create dedicated database users (not postgres superuser)
- Consider using environment variables for credentials
- Restrict database user privileges to only what's needed
- Enable SSL connections for production 