from flask import request, jsonify
from apps.utils.db import SessionLocal
from apps.services.task_service import TaskService
from apps.services.project_service import ProjectService
from apps.models.task import TaskStatus, TaskPriority
from apps.validations.task_validation import validate_task_creation, validate_task_update
from datetime import datetime


class TaskController:
    
    @staticmethod
    def create_task(current_user):
        data = request.get_json()
        
        is_valid, message = validate_task_creation(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        title = data['title'].strip()
        description = data.get('description', '').strip()
        project_id = data['project_id']
        assignee_id = data.get('assignee_id')
        due_date = data.get('due_date')
        priority = data.get('priority', 'medium')
        
        try:
            priority = TaskPriority(priority)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Priority không hợp lệ'
            }), 400
        
        if due_date:
            try:
                due_date = datetime.fromisoformat(due_date)
            except:
                return jsonify({
                    'success': False,
                    'message': 'Format ngày không hợp lệ'
                }), 400
        
        db = SessionLocal()
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Dự án không tồn tại'
                }), 404
            
            success, message, task = TaskService.create_task(
                db, title, description, project_id,
                current_user['user_id'], assignee_id, priority, due_date
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message,
                'data': TaskService.task_to_dict(task)
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
    def get_task(current_user, task_id):
        db = SessionLocal()
        try:
            task = TaskService.get_task_by_id(db, task_id)
            
            if not task:
                return jsonify({
                    'success': False,
                    'message': 'Task không tồn tại'
                }), 404
            
            return jsonify({
                'success': True,
                'data': TaskService.task_to_dict(task)
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
    def get_tasks_by_project(current_user, project_id):
        db = SessionLocal()
        try:
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', 100))
            
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Dự án không tồn tại'
                }), 404
            
            tasks = TaskService.get_tasks_by_project(db, project_id, skip, limit)
            
            return jsonify({
                'success': True,
                'data': [TaskService.task_to_dict(t) for t in tasks],
                'count': len(tasks)
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
    def get_my_tasks(current_user):
        db = SessionLocal()
        try:
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', 100))
            
            tasks = TaskService.get_tasks_by_assignee(
                db, current_user['user_id'], skip, limit
            )
            
            return jsonify({
                'success': True,
                'data': [TaskService.task_to_dict(t) for t in tasks],
                'count': len(tasks)
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
    def update_task(current_user, task_id):
        data = request.get_json()
        
        is_valid, message = validate_task_update(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        db = SessionLocal()
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                return jsonify({
                    'success': False,
                    'message': 'Task không tồn tại'
                }), 404
            
            if str(task.creator_id) != current_user['user_id']:
                return jsonify({
                    'success': False,
                    'message': 'Bạn không có quyền sửa task này'
                }), 403
            
            update_data = {}
            if 'title' in data:
                update_data['title'] = data['title'].strip()
            if 'description' in data:
                update_data['description'] = data['description'].strip()
            if 'status' in data:
                try:
                    update_data['status'] = TaskStatus(data['status'])
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Trạng thái không hợp lệ'
                    }), 400
            if 'priority' in data:
                try:
                    update_data['priority'] = TaskPriority(data['priority'])
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Priority không hợp lệ'
                    }), 400
            if 'assignee_id' in data:
                update_data['assignee_id'] = data['assignee_id']
            
            success, message, updated_task = TaskService.update_task(
                db, task_id, **update_data
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message,
                'data': TaskService.task_to_dict(updated_task)
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
    def delete_task(current_user, task_id):
        db = SessionLocal()
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                return jsonify({
                    'success': False,
                    'message': 'Task không tồn tại'
                }), 404
            
            if str(task.creator_id) != current_user['user_id']:
                return jsonify({
                    'success': False,
                    'message': 'Bạn không có quyền xóa task này'
                }), 403
            
            success, message = TaskService.delete_task(db, task_id)
            
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
