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
RESET_TOKEN_EXPIRATION_MINUTES = 15


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
    def create_reset_token(email: str) -> str:
        payload = {
            'email': email,
            'type': 'reset_password',
            'exp': datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRATION_MINUTES),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def verify_reset_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if payload.get('type') == 'reset_password':
                return payload.get('email')
            return None
        except jwt.ExpiredSignatureError:
            return None
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
    def request_reset_password(db: Session, email: str) -> Tuple[bool, str, Optional[str], Optional[str]]:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return False, "Email không tồn tại trong hệ thống", None, None
        
        if not user.is_active:
            return False, "Tài khoản đã bị vô hiệu hóa", None, None
        
        reset_token = AuthService.create_reset_token(email)
        
        return True, "Email đặt lại mật khẩu đã được gửi", reset_token, user.username
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> Tuple[bool, str, Optional[str]]:
        email = AuthService.verify_reset_token(token)
        
        if not email:
            return False, "Token không hợp lệ hoặc đã hết hạn", None
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return False, "Email không tồn tại trong hệ thống", None
        
        if not user.is_active:
            return False, "Tài khoản đã bị vô hiệu hóa", None
        
        user.password_hash = AuthService.hash_password(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        
        new_token = AuthService.create_token(user.id, user.username)
        
        return True, "Đặt lại mật khẩu thành công", new_token
    
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

