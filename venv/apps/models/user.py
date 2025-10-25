"""
User model - Quản lý người dùng
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owned_projects = relationship(
        "Project", 
        back_populates="owner", 
        foreign_keys="Project.owner_id"
    )
    assigned_tasks = relationship(
        "Task", 
        back_populates="assignee", 
        foreign_keys="Task.assignee_id"
    )
    created_tasks = relationship(
        "Task", 
        back_populates="creator", 
        foreign_keys="Task.creator_id"
    )
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
