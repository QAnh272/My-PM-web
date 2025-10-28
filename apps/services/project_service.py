from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from apps.models.project import Project, ProjectStatus
from apps.models.user import User


class ProjectService:
    
    @staticmethod
    def create_project(db: Session, name: str, description: str, 
                      owner_id: str, start_date: datetime = None, 
                      end_date: datetime = None) -> Tuple[bool, str, Optional[Project]]:
        try:
            new_project = Project(
                name=name,
                description=description,
                status=ProjectStatus.PLANNING,
                owner_id=owner_id,
                start_date=start_date,
                end_date=end_date
            )
            
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            
            return True, "Tạo dự án thành công", new_project
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi tạo dự án: {str(e)}", None
    
    @staticmethod
    def get_project_by_id(db: Session, project_id: str) -> Optional[Project]:
        try:
            return db.query(Project).filter(Project.id == project_id).first()
        except:
            return None
    
    @staticmethod
    def get_projects_by_owner(db: Session, owner_id: str, 
                             skip: int = 0, limit: int = 100) -> List[Project]:
        return db.query(Project)\
            .filter(Project.owner_id == owner_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_all_projects(db: Session, skip: int = 0, 
                        limit: int = 100) -> List[Project]:
        return db.query(Project).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_project(db: Session, project_id: str, 
                      **kwargs) -> Tuple[bool, str, Optional[Project]]:
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Dự án không tồn tại", None
            
            for key, value in kwargs.items():
                if hasattr(project, key) and value is not None:
                    setattr(project, key, value)
            
            db.commit()
            db.refresh(project)
            
            return True, "Cập nhật dự án thành công", project
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi cập nhật: {str(e)}", None
    
    @staticmethod
    def delete_project(db: Session, project_id: str) -> Tuple[bool, str]:
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False, "Dự án không tồn tại"
            
            db.delete(project)
            db.commit()
            
            return True, "Xóa dự án thành công"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi xóa: {str(e)}"
    
    @staticmethod
    def change_project_status(db: Session, project_id: str, 
                             status: ProjectStatus) -> Tuple[bool, str, Optional[Project]]:
        return ProjectService.update_project(db, project_id, status=status)
    
    @staticmethod
    def project_to_dict(project: Project) -> dict:
        return project.to_dict()
