from flask import Blueprint
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.controllers import AuthController
from apps.middlewares import token_required

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


@auth_router.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """
    GET /api/auth/user/<user_id>
    Headers: Authorization: Bearer <token>
    """
    return AuthController.get_current_user(current_user, user_id)


@auth_router.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    POST /api/auth/logout
    Headers: Authorization: Bearer <token>
    """
    return AuthController.logout(current_user)


@auth_router.route('/request-reset-password', methods=['POST'])
def request_reset_password():
    """
    POST /api/auth/request-reset-password
    Body: {email}
    """
    return AuthController.request_reset_password()


@auth_router.route('/reset-password', methods=['POST'])
def reset_password():
    """
    POST /api/auth/reset-password
    Body: {token, new_password}
    """
    return AuthController.reset_password()
