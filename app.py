"""
Main application file for Project Management System
"""
import sys
import os
from pathlib import Path
from datetime import timedelta
sys.path.insert(0, str(Path(__file__).parent / 'venv' / 'apps'))

from flask import Flask, jsonify, session
from flask_session import Session
from apps.utils.db import init_db, get_db
from apps.models import User, Project, Task, Comment
from apps.services.email_service import EmailService

sys.path.insert(0, str(Path(__file__).parent / 'venv' / 'apps'))
from apps.routers import auth_router
from apps.routers.project_router import project_router
from apps.routers.task_router import task_router

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

Session(app)
EmailService.init_mail(app)

app.register_blueprint(auth_router)
app.register_blueprint(project_router)
app.register_blueprint(task_router)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Project Management System API",
        "version": "1.0.0"
    })


@app.route('/health')
def health():
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
