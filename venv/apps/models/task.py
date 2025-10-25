"""
Task model - Quản lý công việc
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class TaskStatus(enum.Enum):
    """Trạng thái công việc"""
    TODO = "todo"                  # Chưa làm
    IN_PROGRESS = "in_progress"    # Đang làm
    IN_REVIEW = "in_review"        # Đang review
    DONE = "done"                  # Hoàn thành


class TaskPriority(enum.Enum):
    """Độ ưu tiên công việc"""
    LOW = "low"                    # Thấp
    MEDIUM = "medium"              # Trung bình
    HIGH = "high"                  # Cao
    URGENT = "urgent"              # Khẩn cấp


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"))
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship(
        "User", 
        back_populates="assigned_tasks", 
        foreign_keys=[assignee_id]
    )
    creator = relationship(
        "User", 
        back_populates="created_tasks", 
        foreign_keys=[creator_id]
    )
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.title}>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value if self.status else None,
            'priority': self.priority.value if self.priority else None,
            'project_id': self.project_id,
            'assignee_id': self.assignee_id,
            'creator_id': self.creator_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
