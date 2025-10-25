"""
Main application file for Project Management System
"""
import sys
import os
from pathlib import Path
from datetime import timedelta

# Add venv/apps to Python path
sys.path.insert(0, str(Path(__file__).parent / 'venv' / 'apps'))

from flask import Flask, jsonify, session
from flask_session import Session
from database import init_db, get_db
from models import User, Project, Task, Comment

# Import routers
sys.path.insert(0, str(Path(__file__).parent / 'venv' / 'apps'))
from apps.routers import auth_router

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize Session
Session(app)

# Register Blueprints
app.register_blueprint(auth_router)


@app.route('/')
def home():
    """Home route"""
    return jsonify({
        "message": "Welcome to Project Management System API",
        "version": "1.0.0"
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Try to connect to database
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    # Initialize database
    print("Initializing database...")
    init_db()
    
    # Run the app
    print("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
