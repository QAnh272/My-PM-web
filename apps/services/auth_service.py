"""
Authentication Service - Business logic cho authentication
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
import sys
from pathlib import Path
import os

# Add models to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from apps.models.user import User

# JWT Configuration
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


class AuthService:
    """Service xử lý authentication logic"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password với bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def create_token(user_id: int, username: str) -> str:
        """Tạo JWT token"""
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """Decode JWT token"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def register_user(db: Session, username: str, email: str, 
                     full_name: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Đăng ký user mới
        
        Returns:
            Tuple (success, message, user)
        """
        # Kiểm tra username đã tồn tại
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return False, "Username đã tồn tại", None
        
        # Kiểm tra email đã tồn tại
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            return False, "Email đã được sử dụng", None
        
        # Hash password
        hashed_password = AuthService.hash_password(password)
        
        # Tạo user mới
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
            return True, "Đăng ký thành công", new_user
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi tạo user: {str(e)}", None
    
    @staticmethod
    def login_user(db: Session, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Đăng nhập user
        
        Returns:
            Tuple (success, message, user)
        """
        # Tìm user
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return False, "Username hoặc password không đúng", None
        
        # Kiểm tra user có active không
        if not user.is_active:
            return False, "Tài khoản đã bị vô hiệu hóa", None
        
        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            return False, "Username hoặc password không đúng", None
        
        return True, "Đăng nhập thành công", user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Lấy user theo ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def user_to_dict(user: User) -> Dict[str, Any]:
        """Convert User model sang dictionary"""
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }
