"""
Authentication Middleware
"""
from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
JWT_ALGORITHM = 'HS256'


def token_required(f):
    """
    Middleware yêu cầu JWT token hợp lệ
    
    Usage:
        @app.route('/api/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'user_id': current_user['user_id']})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Lấy token từ header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Token format không hợp lệ. Sử dụng: Bearer <token>'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token không được cung cấp'
            }), 401
        
        # Decode token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token đã hết hạn'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token không hợp lệ'
            }), 401
        
        # Pass user info vào function
        return f(current_user, *args, **kwargs)
    
    return decorated


def optional_token(f):
    """
    Middleware cho phép truy cập với hoặc không có token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
                current_user = payload
            except (IndexError, AttributeError, jwt.InvalidTokenError):
                pass
        
        return f(current_user, *args, **kwargs)
    
    return decorated
