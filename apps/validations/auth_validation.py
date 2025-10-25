"""
Authentication Validations
"""
import re
from typing import Tuple, Dict, Any


def validate_register_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate dữ liệu đăng ký
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not data:
        return False, "Không có dữ liệu"
    
    # Kiểm tra các field bắt buộc
    required_fields = ['username', 'email', 'full_name', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Thiếu field bắt buộc: {field}"
    
    # Validate username
    username = data['username'].strip()
    if len(username) < 3 or len(username) > 50:
        return False, "Username phải có 3-50 ký tự"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username chỉ được chứa chữ, số, gạch dưới"
    
    # Validate email
    email = data['email'].strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Email không hợp lệ"
    
    # Validate password
    password = data['password']
    if len(password) < 8:
        return False, "Password phải có ít nhất 8 ký tự"
    
    if len(password) > 128:
        return False, "Password không được vượt quá 128 ký tự"
    
    # Kiểm tra chữ hoa
    if not any(c.isupper() for c in password):
        return False, "Password phải có ít nhất 1 chữ cái viết hoa"
    
    # Kiểm tra chữ thường
    if not any(c.islower() for c in password):
        return False, "Password phải có ít nhất 1 chữ cái viết thường"
    
    # Kiểm tra số
    if not any(c.isdigit() for c in password):
        return False, "Password phải có ít nhất 1 chữ số"
    
    # Kiểm tra ký tự đặc biệt
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Password phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*...)"
    
    return True, ""


def validate_login_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate dữ liệu đăng nhập
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if not data:
        return False, "Không có dữ liệu"
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username:
        return False, "Username là bắt buộc"
    
    if not password:
        return False, "Password là bắt buộc"
    
    return True, ""


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """Validate username"""
    if len(username) < 3 or len(username) > 50:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None


def validate_password(password: str) -> bool:
    """
    Validate password
    - Độ dài: 8-128 ký tự
    - Phải có ít nhất 1 chữ hoa
    - Phải có ít nhất 1 chữ thường
    - Phải có ít nhất 1 chữ số
    - Phải có ít nhất 1 ký tự đặc biệt
    """
    if len(password) < 8 or len(password) > 128:
        return False
    
    if not any(c.isupper() for c in password):
        return False
    
    if not any(c.islower() for c in password):
        return False
    
    if not any(c.isdigit() for c in password):
        return False
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False
    
    return True
