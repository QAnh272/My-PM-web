"""
Models module - Import từ venv/apps/models package
File này giữ lại để backward compatibility
"""
import sys
from pathlib import Path

# Add venv/apps to Python path
sys.path.insert(0, str(Path(__file__).parent / 'venv' / 'apps'))

# Import all models from the models package
from models import (
    User,
    Project, ProjectStatus,
    Task, TaskStatus, TaskPriority,
    Comment
)

__all__ = [
    'User',
    'Project', 'ProjectStatus',
    'Task', 'TaskStatus', 'TaskPriority',
    'Comment'
]
