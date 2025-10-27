"""
Authentication Controller - Xử lý requests và responses
"""
from flask import request, jsonify
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.utils.db import SessionLocal
from apps.services import AuthService
from apps.validations import validate_register_data, validate_login_data


class AuthController:
    
    @staticmethod
    def register():
        data = request.get_json()
        
        is_valid, error_msg = validate_register_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error_msg
            }), 400
        
        username = data['username'].strip()
        email = data['email'].strip()
        full_name = data['full_name'].strip()
        password = data['password']
        
        db = SessionLocal()
        try:
            success, message, user, token = AuthService.register_user(
                db, username, email, full_name, password
            )
            
            if not success:
                status_code = 409 if "đã tồn tại" in message or "đã được sử dụng" in message else 400
                return jsonify({
                    'success': False,
                    'message': message
                }), status_code
            
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
        data = request.get_json()
        
        is_valid, error_msg = validate_login_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error_msg
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        db = SessionLocal()
        try:
            success, message, user, token = AuthService.login_user(db, username, password)
            
            if not success:
                status_code = 403 if "vô hiệu hóa" in message else 401
                return jsonify({
                    'success': False,
                    'message': message
                }), status_code
            
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
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def logout(current_user):
        try:
            success, message = AuthService.logout_user()
            
            return jsonify({
                'success': success,
                'message': message
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
    
    @staticmethod
    def refresh_token(current_user):
        try:
            success, message, new_token = AuthService.refresh_user_token(
                current_user['user_id'],
                current_user['username']
            )
            
            return jsonify({
                'success': success,
                'message': message,
                'data': {
                    'token': new_token
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
