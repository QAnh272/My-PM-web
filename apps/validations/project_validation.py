from typing import Tuple

def validate_project_creation(data: dict) -> Tuple[bool, str]:
    if not data.get('name'):
        return False, "Project name is required"
    
    if len(data['name'].strip()) < 3:
        return False, "Project name must be at least 3 characters"
    
    if len(data['name']) > 100:
        return False, "Project name must not exceed 100 characters"
    
    if data.get('description') and len(data['description']) > 500:
        return False, "Project description must not exceed 500 characters"
    
    if data.get('status') and data['status'] not in ['PLANNING', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED', 'CANCELLED']:
        return False, "Invalid project status"
    
    return True, "Valid"

def validate_project_update(data: dict) -> Tuple[bool, str]:
    if data.get('name'):
        if len(data['name'].strip()) < 3:
            return False, "Project name must be at least 3 characters"
        
        if len(data['name']) > 100:
            return False, "Project name must not exceed 100 characters"
    
    if data.get('description') and len(data['description']) > 500:
        return False, "Project description must not exceed 500 characters"
    
    if data.get('status') and data['status'] not in ['PLANNING', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED', 'CANCELLED']:
        return False, "Invalid project status"
    
    return True, "Valid"
