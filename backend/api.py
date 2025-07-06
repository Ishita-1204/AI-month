from flask import Blueprint, request, jsonify
from backend.models import db, User, Session
from flask_socketio import emit
import uuid
from datetime import datetime, date

api_bp = Blueprint('api', __name__)

def send_welcome_announcement(username, is_new_user=False):
    """Send welcome announcement with daily tasks"""
    from app import socketio
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    if is_new_user:
        title = f"🎉 Welcome to AI Month, {username}!"
        body = f"""
        <strong>Welcome to AI Month!</strong><br><br>
        <strong>Today's Tasks ({current_date}):</strong><br>
        1. 🧠 Complete the Machine Learning tutorial<br>
        2. 🤖 Build your first AI chatbot<br>
        3. 📊 Analyze a dataset with Python<br><br>
        <em>Ready to dive into the world of AI? Let's get started!</em>
        """
    else:
        title = f"👋 Welcome back, {username}!"
        body = f"""
        <strong>Welcome back to AI Month!</strong><br><br>
        <strong>Today's Tasks ({current_date}):</strong><br>
        1. 🧠 Complete the Machine Learning tutorial<br>
        2. 🤖 Build your first AI chatbot<br>
        3. 📊 Analyze a dataset with Python<br><br>
        <em>Continue your AI journey!</em>
        """
    
    announcement = {
        'title': title,
        'body': body,
        'timestamp': datetime.now().timestamp(),
        'username': username,
        'type': 'welcome_banner'
    }
    socketio.emit('new_announcement', announcement)
    return announcement

def get_todays_announcements():
    """Get all announcements for today"""
    today = date.today()
    from app import Announcement
    
    # Get announcements created today
    todays_announcements = Announcement.query.filter(
        db.func.date(Announcement.created_at) == today
    ).order_by(Announcement.created_at.desc()).all()
    
    return [announcement.to_dict() for announcement in todays_announcements]

@api_bp.route('/api/todays-announcements', methods=['GET'])
def todays_announcements():
    """API endpoint to get today's announcements"""
    try:
        announcements = get_todays_announcements()
        return jsonify({
            'announcements': announcements,
            'count': len(announcements)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409
    
    # Create new user
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    # Send welcome announcement for new user
    announcement = send_welcome_announcement(username, is_new_user=True)
    
    return jsonify({'message': 'User created successfully', 'announcement': announcement}), 201

@api_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Find user in database
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        # Create session token
        token = str(uuid.uuid4())
        session = Session(token=token, username=username)
        db.session.add(session)
        db.session.commit()
        
        # Send welcome back announcement
        announcement = send_welcome_announcement(username, is_new_user=False)
        
        return jsonify({'token': token, 'announcement': announcement}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify if a token is valid"""
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1]
        
        # Find session
        session = Session.query.filter_by(token=token).first()
        if session:
            return jsonify({'valid': True, 'username': session.username}), 200
    
    return jsonify({'valid': False}), 401

@api_bp.route('/signout', methods=['POST'])
def signout():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1]
        
        # Find and delete session
        session = Session.query.filter_by(token=token).first()
        if session:
            db.session.delete(session)
            db.session.commit()
            return jsonify({'message': 'Signed out'}), 200
    
    return jsonify({'error': 'Invalid token'}), 401 