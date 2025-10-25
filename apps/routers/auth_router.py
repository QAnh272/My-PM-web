"""
Authentication Routes
"""
from flask import Blueprint
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.controllers import AuthController
from apps.middlewares import token_required

# Create blueprint
auth_router = Blueprint('auth', __name__, url_prefix='/api/auth')


# Routes
@auth_router.route('/register', methods=['POST'])
def register():
    """
    POST /api/auth/register
    Body: {username, email, full_name, password}
    """
    return AuthController.register()


@auth_router.route('/login', methods=['POST'])
def login():
    """
    POST /api/auth/login
    Body: {username, password}
    """
    return AuthController.login()


@auth_router.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    GET /api/auth/me
    Headers: Authorization: Bearer <token>
    """
    return AuthController.get_current_user(current_user)


@auth_router.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    POST /api/auth/logout
    Headers: Authorization: Bearer <token>
    """
    return AuthController.logout(current_user)


@auth_router.route('/refresh', methods=['POST'])
@token_required
def refresh_token(current_user):
    """
    POST /api/auth/refresh
    Headers: Authorization: Bearer <token>
    """
    return AuthController.refresh_token(current_user)
