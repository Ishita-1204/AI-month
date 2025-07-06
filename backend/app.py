from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
import secrets
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration - using SQLite for easier testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_month.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes
CORS(app)

# Initialize database
db = SQLAlchemy(app)

# Define models directly in this file to avoid import issues
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed passwords
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Session {self.token}>'

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(80), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': self.created_by
        }

def create_tables():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        
        # Create default users if they don't exist
        if not User.query.filter_by(username='alice').first():
            alice = User(username='alice', password=generate_password_hash('password1'))
            db.session.add(alice)
            
        if not User.query.filter_by(username='bob').first():
            bob = User(username='bob', password=generate_password_hash('password2'))
            db.session.add(bob)
            
        db.session.commit()

def generate_token():
    """Generate a secure token"""
    return secrets.token_urlsafe(32)

def verify_token(token):
    """Verify if a token is valid and return the username"""
    session = Session.query.filter_by(token=token).first()
    if session and session.created_at > datetime.utcnow() - timedelta(hours=24):
        return session.username
    return None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('home.html')

@app.route('/api/signin', methods=['POST'])
def signin():
    """API endpoint for user signin"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check if user exists and password is correct
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Generate new token
            token = generate_token()
            
            # Remove old sessions for this user
            Session.query.filter_by(username=username).delete()
            
            # Create new session
            session = Session(token=token, username=username)
            db.session.add(session)
            db.session.commit()
            
            return jsonify({
                'message': 'Sign in successful',
                'username': username,
                'token': token
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    """API endpoint for user signup"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        
        # Generate token for new user
        token = generate_token()
        session = Session(token=token, username=username)
        db.session.add(session)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Sign up successful',
            'username': username,
            'token': token
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/signout', methods=['POST'])
def signout():
    """API endpoint for user signout"""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({'error': 'Token is required'}), 400
        
        token = data['token']
        
        # Remove session
        session = Session.query.filter_by(token=token).first()
        if session:
            db.session.delete(session)
            db.session.commit()
        
        return jsonify({
            'message': 'Sign out successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify', methods=['GET'])
def verify():
    """API endpoint to verify if server is running"""
    return jsonify({
        'message': 'Server is running',
        'status': 'ok'
    }), 200

@app.route('/api/verify-token', methods=['POST'])
def verify_token_endpoint():
    """API endpoint to verify a token"""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({'error': 'Token is required'}), 400
        
        token = data['token']
        username = verify_token(token)
        
        if username:
            return jsonify({
                'valid': True,
                'username': username
            }), 200
        else:
            return jsonify({
                'valid': False
            }), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/announce', methods=['POST'])
def announce():
    """API endpoint to create new announcements"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data or 'body' not in data or 'token' not in data:
            return jsonify({'error': 'Title, body, and token are required'}), 400
        
        title = data['title']
        body = data['body']
        token = data['token']
        
        # Verify token
        username = verify_token(token)
        if not username:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Create new announcement
        new_announcement = Announcement(
            title=title,
            body=body,
            created_by=username
        )
        
        db.session.add(new_announcement)
        db.session.commit()
        
        return jsonify({
            'message': 'Announcement created successfully',
            'announcement': new_announcement.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    """API endpoint to get all announcements"""
    try:
        announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
        
        return jsonify({
            'announcements': [announcement.to_dict() for announcement in announcements]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todays-announcements', methods=['GET'])
def get_todays_announcements():
    """API endpoint to get today's announcements"""
    try:
        from datetime import date
        
        today = date.today()
        todays_announcements = Announcement.query.filter(
            db.func.date(Announcement.created_at) == today
        ).order_by(Announcement.created_at.desc()).all()
        
        return jsonify({
            'announcements': [announcement.to_dict() for announcement in todays_announcements],
            'count': len(todays_announcements)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Month Dashboard Backend...")
    print("🌐 Server available at: http://localhost:5000")
    print("📢 API endpoints available at: http://localhost:5000/api/*")
    print("=" * 50)
    
    # Create database tables
    create_tables()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 