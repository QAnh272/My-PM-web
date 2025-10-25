"""
Authentication Controller - Xử lý requests và responses
"""
from flask import request, jsonify, session
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import SessionLocal
from apps.services import AuthService
from apps.validations import validate_register_data, validate_login_data


class AuthController:
    """Controller xử lý authentication"""
    
    @staticmethod
    def register():
        """Xử lý đăng ký user mới"""
        data = request.get_json()
        
        # Validate input
        is_valid, error_msg = validate_register_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error_msg
            }), 400
        
        # Lấy dữ liệu
        username = data['username'].strip()
        email = data['email'].strip()
        full_name = data['full_name'].strip()
        password = data['password']
        
        # Gọi service
        db = SessionLocal()
        try:
            success, message, user = AuthService.register_user(
                db, username, email, full_name, password
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 409 if "đã tồn tại" in message or "đã được sử dụng" in message else 400
            
            # Tạo token
            token = AuthService.create_token(user.id, user.username)
            
            return jsonify({
                'success': True,
                'message': message,
                'data': {
                    'user': AuthService.user_to_dict(user),
                    'token': token
                }
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def login():
        """Xử lý đăng nhập"""
        data = request.get_json()
        
        # Validate input
        is_valid, error_msg = validate_login_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error_msg
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Gọi service
        db = SessionLocal()
        try:
            success, message, user = AuthService.login_user(db, username, password)
            
            if not success:
                status_code = 403 if "vô hiệu hóa" in message else 401
                return jsonify({
                    'success': False,
                    'message': message
                }), status_code
            
            # Tạo token
            token = AuthService.create_token(user.id, user.username)
            
            # Tạo session
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            
            return jsonify({
                'success': True,
                'message': message,
                'data': {
                    'user': AuthService.user_to_dict(user),
                    'token': token
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def get_current_user(current_user):
        """Lấy thông tin user hiện tại"""
        db = SessionLocal()
        try:
            user = AuthService.get_user_by_id(db, current_user['user_id'])
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User không tồn tại'
                }), 404
            
            return jsonify({
                'success': True,
                'data': AuthService.user_to_dict(user)
            }), 200
            
        finally:
            db.close()
    
    @staticmethod
    def logout(current_user):
        """Đăng xuất"""
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Đăng xuất thành công'
        }), 200
    
    @staticmethod
    def refresh_token(current_user):
        """Làm mới token"""
        new_token = AuthService.create_token(
            current_user['user_id'],
            current_user['username']
        )
        
        return jsonify({
            'success': True,
            'message': 'Token đã được làm mới',
            'data': {
                'token': new_token
            }
        }), 200
