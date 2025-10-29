from flask import request, jsonify
from apps.utils.db import SessionLocal
from apps.services.comment_service import CommentService
from apps.services.task_service import TaskService
from apps.validations.comment_validation import (
    validate_create_comment, 
    validate_update_comment,
    validate_comment_id
)


class CommentController:
    
    @staticmethod
    def create_comment(current_user):
        """Create a new comment on a task."""
        validation_error = validate_create_comment()
        if validation_error:
            return validation_error
        
        data = request.get_json()
        content = data['content'].strip()
        task_id = data['task_id']
        
        db = SessionLocal()
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                return jsonify({
                    'success': False,
                    'message': 'Task không tồn tại'
                }), 404
            
            success, message, comment = CommentService.create_comment(
                db, content, task_id, current_user['user_id']
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message,
                'data': CommentService.comment_to_dict(comment, include_author=True)
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def get_comment(current_user, comment_id):
        """Get a specific comment by ID."""
        validation_error = validate_comment_id(comment_id)
        if validation_error:
            return validation_error
        
        db = SessionLocal()
        try:
            comment = CommentService.get_comment_by_id(db, comment_id)
            
            if not comment:
                return jsonify({
                    'success': False,
                    'message': 'Comment không tồn tại'
                }), 404
            
            return jsonify({
                'success': True,
                'data': CommentService.comment_to_dict(comment, include_author=True)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def get_comments_by_task(current_user, task_id):
        """Get all comments for a specific task."""
        db = SessionLocal()
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                return jsonify({
                    'success': False,
                    'message': 'Task không tồn tại'
                }), 404
            
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 20, type=int)
            skip = (page - 1) * limit
            
            comments = CommentService.get_comments_by_task(db, task_id, skip, limit)
            total = CommentService.count_comments_by_task(db, task_id)
            
            return jsonify({
                'success': True,
                'data': {
                    'comments': [CommentService.comment_to_dict(c, include_author=True) for c in comments],
                    'pagination': {
                        'page': page,
                        'limit': limit,
                        'total': total,
                        'pages': (total + limit - 1) // limit
                    }
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def get_my_comments(current_user):
        """Get all comments by the current user."""
        db = SessionLocal()
        try:
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 20, type=int)
            skip = (page - 1) * limit
            
            comments = CommentService.get_comments_by_author(
                db, current_user['user_id'], skip, limit
            )
            
            return jsonify({
                'success': True,
                'data': {
                    'comments': [CommentService.comment_to_dict(c, include_author=True) for c in comments],
                    'pagination': {
                        'page': page,
                        'limit': limit
                    }
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def update_comment(current_user, comment_id):
        """Update a comment (only by author)."""
        validation_error = validate_comment_id(comment_id)
        if validation_error:
            return validation_error
        
        validation_error = validate_update_comment()
        if validation_error:
            return validation_error
        
        data = request.get_json()
        content = data['content'].strip()
        
        db = SessionLocal()
        try:
            comment = CommentService.get_comment_by_id(db, comment_id)
            
            if not comment:
                return jsonify({
                    'success': False,
                    'message': 'Comment không tồn tại'
                }), 404
            
            if not CommentService.is_comment_author(comment, current_user['user_id']):
                return jsonify({
                    'success': False,
                    'message': 'Bạn không có quyền sửa comment này'
                }), 403
            
            success, message, updated_comment = CommentService.update_comment(
                db, comment_id, content
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message,
                'data': CommentService.comment_to_dict(updated_comment, include_author=True)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()
    
    @staticmethod
    def delete_comment(current_user, comment_id):
        """Delete a comment (only by author)."""
        validation_error = validate_comment_id(comment_id)
        if validation_error:
            return validation_error
        
        db = SessionLocal()
        try:
            comment = CommentService.get_comment_by_id(db, comment_id)
            
            if not comment:
                return jsonify({
                    'success': False,
                    'message': 'Comment không tồn tại'
                }), 404
            
            if not CommentService.is_comment_author(comment, current_user['user_id']):
                return jsonify({
                    'success': False,
                    'message': 'Bạn không có quyền xóa comment này'
                }), 403
            
            success, message = CommentService.delete_comment(db, comment_id)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Đã xảy ra lỗi',
                'error': str(e)
            }), 500
        finally:
            db.close()


__all__ = ['CommentController']
