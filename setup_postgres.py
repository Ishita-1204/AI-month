import psycopg2
from psycopg2 import sql
import sqlite3
import json

# PostgreSQL connection details
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',  # Connect to default database first
    'user': 'postgres',
    'password': '1204'  # Change this to your actual password
}

def create_database():
    """Create the AI Month database"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(**PG_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create the database
        cursor.execute("CREATE DATABASE ai_month_db")
        print("✅ Database 'ai_month_db' created successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.errors.DuplicateDatabase:
        print("ℹ️ Database 'ai_month_db' already exists")
    except Exception as e:
        print(f"❌ Error creating database: {e}")

def create_tables():
    """Create tables in the new database"""
    # Update config to use the new database
    pg_config = PG_CONFIG.copy()
    pg_config['database'] = 'ai_month_db'
    
    try:
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor()
        
        # Create users table with longer password field
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                token VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(80) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create announcements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(80) NOT NULL
            )
        """)
        
        conn.commit()
        print("✅ Tables created successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

def migrate_data_from_sqlite():
    """Migrate data from SQLite to PostgreSQL"""
    try:
        # Read from SQLite
        sqlite_conn = sqlite3.connect('backend/ai_month.db')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to PostgreSQL
        pg_config = PG_CONFIG.copy()
        pg_config['database'] = 'ai_month_db'
        pg_conn = psycopg2.connect(**pg_config)
        pg_cursor = pg_conn.cursor()
        
        # Migrate users
        sqlite_cursor.execute("SELECT username, password, created_at FROM users")
        users = sqlite_cursor.fetchall()
        
        for user in users:
            pg_cursor.execute("""
                INSERT INTO users (username, password, created_at) 
                VALUES (%s, %s, %s) 
                ON CONFLICT (username) DO NOTHING
            """, user)
        
        # Migrate sessions
        sqlite_cursor.execute("SELECT token, username, created_at FROM sessions")
        sessions = sqlite_cursor.fetchall()
        
        for session in sessions:
            pg_cursor.execute("""
                INSERT INTO sessions (token, username, created_at) 
                VALUES (%s, %s, %s) 
                ON CONFLICT (token) DO NOTHING
            """, session)
        
        # Migrate announcements
        sqlite_cursor.execute("SELECT title, body, created_at, created_by FROM announcements")
        announcements = sqlite_cursor.fetchall()
        
        for announcement in announcements:
            pg_cursor.execute("""
                INSERT INTO announcements (title, body, created_at, created_by) 
                VALUES (%s, %s, %s, %s)
            """, announcement)
        
        pg_conn.commit()
        print(f"✅ Migrated {len(users)} users, {len(sessions)} sessions, {len(announcements)} announcements")
        
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
    except Exception as e:
        print(f"❌ Error migrating data: {e}")

if __name__ == "__main__":
    print("🚀 Setting up PostgreSQL database...")
    create_database()
    create_tables()
    migrate_data_from_sqlite()
    print("✅ PostgreSQL setup complete!")
    print("\n📋 Next steps:")
    print("1. Connect to 'ai_month_db' in pgAdmin")
    print("2. View your tables: users, sessions, announcements")
    print("3. Update backend/app.py to use PostgreSQL instead of SQLite") 