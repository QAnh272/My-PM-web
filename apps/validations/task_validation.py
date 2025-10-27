from typing import Tuple

def validate_task_creation(data: dict) -> Tuple[bool, str]:
    if not data.get('title'):
        return False, "Task title is required"
    
    if len(data['title'].strip()) < 3:
        return False, "Task title must be at least 3 characters"
    
    if len(data['title']) > 200:
        return False, "Task title must not exceed 200 characters"
    
    if not data.get('project_id'):
        return False, "Project ID is required"
    
    if data.get('description') and len(data['description']) > 1000:
        return False, "Task description must not exceed 1000 characters"
    
    if data.get('status') and data['status'] not in ['TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE']:
        return False, "Invalid task status"
    
    if data.get('priority') and data['priority'] not in ['LOW', 'MEDIUM', 'HIGH', 'URGENT']:
        return False, "Invalid task priority"
    
    return True, "Valid"

def validate_task_update(data: dict) -> Tuple[bool, str]:
    if data.get('title'):
        if len(data['title'].strip()) < 3:
            return False, "Task title must be at least 3 characters"
        
        if len(data['title']) > 200:
            return False, "Task title must not exceed 200 characters"
    
    if data.get('description') and len(data['description']) > 1000:
        return False, "Task description must not exceed 1000 characters"
    
    if data.get('status') and data['status'] not in ['TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE']:
        return False, "Invalid task status"
    
    if data.get('priority') and data['priority'] not in ['LOW', 'MEDIUM', 'HIGH', 'URGENT']:
        return False, "Invalid task priority"
    
    return True, "Valid"
