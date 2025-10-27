"""
Authentication Service - Business logic cho authentication
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from flask import session
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent))
from apps.models.user import User

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def create_token(user_id, username: str) -> str:
        payload = {
            'user_id': str(user_id),
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def create_session(user: User) -> None:
        session.permanent = True
        session['user_id'] = str(user.id)
        session['username'] = user.username
        session['email'] = user.email
    
    @staticmethod
    def clear_session() -> None:
        session.clear()
    
    @staticmethod
    def register_user(db: Session, username: str, email: str, 
                     full_name: str, password: str) -> Tuple[bool, str, Optional[User], Optional[str]]:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return False, "Username đã tồn tại", None, None
        
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            return False, "Email đã được sử dụng", None, None
        
        hashed_password = AuthService.hash_password(password)
        
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=hashed_password,
            is_active=True
        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            token = AuthService.create_token(new_user.id, new_user.username)
            AuthService.create_session(new_user)
            
            return True, "Đăng ký thành công", new_user, token
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi tạo user: {str(e)}", None, None
    
    
    @staticmethod
    def login_user(db: Session, username: str, password: str) -> Tuple[bool, str, Optional[User], Optional[str]]:
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return False, "Username hoặc password không đúng", None, None
        
        if not user.is_active:
            return False, "Tài khoản đã bị vô hiệu hóa", None, None
        
        if not AuthService.verify_password(password, user.password_hash):
            return False, "Username hoặc password không đúng", None, None
        
        token = AuthService.create_token(user.id, user.username)
        AuthService.create_session(user)
        
        return True, "Đăng nhập thành công", user, token
    
    @staticmethod
    def logout_user() -> Tuple[bool, str]:
        AuthService.clear_session()
        return True, "Đăng xuất thành công"
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.id == user_id).first()
        except:
            return None
    
    @staticmethod
    def refresh_user_token(user_id: str, username: str) -> Tuple[bool, str, str]:
        new_token = AuthService.create_token(user_id, username)
        return True, "Token đã được làm mới", new_token
    
    @staticmethod
    def user_to_dict(user: User) -> Dict[str, Any]:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }

