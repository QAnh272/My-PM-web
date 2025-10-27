"""
Task Service - Business logic cho task management
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from apps.models.task import Task, TaskStatus, TaskPriority


class TaskService:
    
    @staticmethod
    def create_task(db: Session, title: str, description: str,
                   project_id: str, creator_id: str,
                   assignee_id: str = None, priority: TaskPriority = TaskPriority.MEDIUM,
                   due_date: datetime = None) -> Tuple[bool, str, Optional[Task]]:
        try:
            new_task = Task(
                title=title,
                description=description,
                status=TaskStatus.TODO,
                priority=priority,
                project_id=project_id,
                assignee_id=assignee_id,
                creator_id=creator_id,
                due_date=due_date
            )
            
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            
            return True, "Tạo task thành công", new_task
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi tạo task: {str(e)}", None
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: str) -> Optional[Task]:
        try:
            return db.query(Task).filter(Task.id == task_id).first()
        except:
            return None
    
    @staticmethod
    def get_tasks_by_project(db: Session, project_id: str,
                            skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task)\
            .filter(Task.project_id == project_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_tasks_by_assignee(db: Session, assignee_id: str,
                             skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task)\
            .filter(Task.assignee_id == assignee_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_tasks_by_creator(db: Session, creator_id: str,
                            skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task)\
            .filter(Task.creator_id == creator_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def update_task(db: Session, task_id: str,
                   **kwargs) -> Tuple[bool, str, Optional[Task]]:
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                return False, "Task không tồn tại", None
            
            for key, value in kwargs.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
            
            db.commit()
            db.refresh(task)
            
            return True, "Cập nhật task thành công", task
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi cập nhật: {str(e)}", None
    
    @staticmethod
    def delete_task(db: Session, task_id: str) -> Tuple[bool, str]:
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                return False, "Task không tồn tại"
            
            db.delete(task)
            db.commit()
            
            return True, "Xóa task thành công"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi xóa: {str(e)}"
    
    @staticmethod
    def change_task_status(db: Session, task_id: str,
                          status: TaskStatus) -> Tuple[bool, str, Optional[Task]]:
        return TaskService.update_task(db, task_id, status=status)
    
    @staticmethod
    def assign_task(db: Session, task_id: str,
                   assignee_id: str) -> Tuple[bool, str, Optional[Task]]:
        return TaskService.update_task(db, task_id, assignee_id=assignee_id)
    
    @staticmethod
    def task_to_dict(task: Task) -> dict:
        return task.to_dict()
