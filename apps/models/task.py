from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from apps.utils.db import Base


class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'status': self.status.value if self.status else None,
            'priority': self.priority.value if self.priority else None,
            'project_id': str(self.project_id),
            'assignee_id': str(self.assignee_id) if self.assignee_id else None,
            'creator_id': str(self.creator_id),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
