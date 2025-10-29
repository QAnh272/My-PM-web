from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from datetime import datetime

from apps.models.comment import Comment


class CommentService:
    
    @staticmethod
    def create_comment(db: Session, content: str, task_id: str, 
                      author_id: str) -> Tuple[bool, str, Optional[Comment]]:
        """Create a new comment on a task."""
        try:
            new_comment = Comment(
                content=content,
                task_id=task_id,
                author_id=author_id
            )
            
            db.add(new_comment)
            db.commit()
            db.refresh(new_comment)
            
            return True, "Tạo comment thành công", new_comment
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi tạo comment: {str(e)}", None
    
    @staticmethod
    def get_comment_by_id(db: Session, comment_id: str) -> Optional[Comment]:
        """Get a comment by ID."""
        try:
            return db.query(Comment).filter(Comment.id == comment_id).first()
        except:
            return None
    
    @staticmethod
    def get_comments_by_task(db: Session, task_id: str, 
                            skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments for a specific task."""
        return db.query(Comment)\
            .filter(Comment.task_id == task_id)\
            .order_by(Comment.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_comments_by_author(db: Session, author_id: str,
                              skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments by a specific author."""
        return db.query(Comment)\
            .filter(Comment.author_id == author_id)\
            .order_by(Comment.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def update_comment(db: Session, comment_id: str, 
                      content: str) -> Tuple[bool, str, Optional[Comment]]:
        """Update comment content."""
        try:
            comment = CommentService.get_comment_by_id(db, comment_id)
            if not comment:
                return False, "Comment không tồn tại", None
            
            comment.content = content
            comment.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(comment)
            
            return True, "Cập nhật comment thành công", comment
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi cập nhật comment: {str(e)}", None
    
    @staticmethod
    def delete_comment(db: Session, comment_id: str) -> Tuple[bool, str]:
        """Delete a comment."""
        try:
            comment = CommentService.get_comment_by_id(db, comment_id)
            if not comment:
                return False, "Comment không tồn tại"
            
            db.delete(comment)
            db.commit()
            
            return True, "Xóa comment thành công"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khi xóa comment: {str(e)}"
    
    @staticmethod
    def count_comments_by_task(db: Session, task_id: str) -> int:
        """Count total comments for a task."""
        try:
            return db.query(Comment).filter(Comment.task_id == task_id).count()
        except:
            return 0
    
    @staticmethod
    def is_comment_author(comment: Comment, user_id: str) -> bool:
        """Check if user is the author of the comment."""
        return str(comment.author_id) == str(user_id)
    
    @staticmethod
    def comment_to_dict(comment: Comment, include_author: bool = False) -> dict:
        """Convert comment to dictionary."""
        data = comment.to_dict()
        
        if include_author and comment.author:
            data['author'] = {
                'id': str(comment.author.id),
                'username': comment.author.username,
                'full_name': comment.author.full_name
            }
        
        return data


__all__ = ['CommentService']
