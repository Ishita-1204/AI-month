#!/usr/bin/env python3
"""
Simple test script to debug server startup
"""

try:
    print("Testing imports...")
    from flask import Flask, render_template, request, jsonify
    print("✅ Flask imports successful")
    
    from flask_cors import CORS
    print("✅ CORS import successful")
    
    from flask_sqlalchemy import SQLAlchemy
    print("✅ SQLAlchemy import successful")
    
    from werkzeug.security import generate_password_hash, check_password_hash
    print("✅ Werkzeug imports successful")
    
    import time
    import secrets
    from datetime import datetime, timedelta
    import os
    print("✅ Standard library imports successful")
    
    print("All imports successful!")
    
    # Test Flask app creation
    app = Flask(__name__)
    print("✅ Flask app created successfully")
    
    # Test database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("✅ Database configuration successful")
    
    # Test CORS
    CORS(app)
    print("✅ CORS configured successfully")
    
    # Test SQLAlchemy
    db = SQLAlchemy(app)
    print("✅ SQLAlchemy initialized successfully")
    
    print("🎉 All tests passed! Server should start successfully.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 