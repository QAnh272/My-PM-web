import re
from typing import Tuple, Dict, Any


def validate_register_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    if not data:
        return False, "Dữ liệu không được để trống"
    
    required_fields = ['username', 'email', 'full_name', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Thiếu field bắt buộc: {field}"
    
    username = data['username'].strip()
    if len(username) < 3 or len(username) > 50:
        return False, "Username phải có độ dài từ 3-50 ký tự"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username chỉ được chứa chữ cái, số và dấu gạch dưới"
    
    email = data['email'].strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Email không hợp lệ"
    
    password = data['password']
    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự"
    if len(password) > 128:
        return False, "Mật khẩu không được vượt quá 128 ký tự"
    if not any(c.isupper() for c in password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ hoa"
    if not any(c.islower() for c in password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ thường"
    if not any(c.isdigit() for c in password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ số"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt"
    
    return True, "Hợp lệ"


def validate_login_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    if not data:
        return False, "Dữ liệu không được để trống"
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username:
        return False, "Username không được để trống"
    
    if not password:
        return False, "Mật khẩu không được để trống"
    
    return True, "Hợp lệ"


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> bool:
    if len(username) < 3 or len(username) > 50:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None


def validate_password(password: str) -> bool:
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


def validate_reset_password_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    if not data:
        return False, "Dữ liệu không được để trống"
    
    token = data.get('token', '').strip()
    new_password = data.get('new_password', '')
    
    if not token:
        return False, "Token không được để trống"
    
    if not new_password:
        return False, "Mật khẩu mới không được để trống"
    
    if not validate_password(new_password):
        return False, "Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt"
    
    return True, "Hợp lệ"


def validate_request_reset_password(data: Dict[str, Any]) -> Tuple[bool, str]:
    if not data:
        return False, "Dữ liệu không được để trống"
    
    email = data.get('email', '').strip()
    
    if not email:
        return False, "Email không được để trống"
    
    if not validate_email(email):
        return False, "Email không hợp lệ"
    
    return True, "Hợp lệ"
