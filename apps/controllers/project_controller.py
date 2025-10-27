"""
Project Controller
"""
from flask import request, jsonify
from apps.utils.db import SessionLocal
from apps.services.project_service import ProjectService
from apps.models.project import ProjectStatus
from apps.validations.project_validation import validate_project_creation, validate_project_update
from datetime import datetime


class ProjectController:
    
    @staticmethod
    def create_project(current_user):
        data = request.get_json()
        
        is_valid, message = validate_project_creation(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        name = data['name'].strip()
        description = data.get('description', '').strip()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date)
            except:
                return jsonify({
                    'success': False,
                    'message': 'Format ngày bắt đầu không hợp lệ'
                }), 400
        
        if end_date:
            try:
                end_date = datetime.fromisoformat(end_date)
            except:
                return jsonify({
                    'success': False,
                    'message': 'Format ngày kết thúc không hợp lệ'
                }), 400
        
        db = SessionLocal()
        try:
            success, message, project = ProjectService.create_project(
                db, name, description, current_user['user_id'],
                start_date, end_date
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message,
                'data': ProjectService.project_to_dict(project)
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
    def get_project(current_user, project_id):
        db = SessionLocal()
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Dự án không tồn tại'
                }), 404
            
            return jsonify({
                'success': True,
                'data': ProjectService.project_to_dict(project)
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
    def get_my_projects(current_user):
        db = SessionLocal()
        try:
            skip = int(request.args.get('skip', 0))
            limit = int(request.args.get('limit', 100))
            
            projects = ProjectService.get_projects_by_owner(
                db, current_user['user_id'], skip, limit
            )
            
            return jsonify({
                'success': True,
                'data': [ProjectService.project_to_dict(p) for p in projects],
                'count': len(projects)
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
    def update_project(current_user, project_id):
        data = request.get_json()
        
        is_valid, message = validate_project_update(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        db = SessionLocal()
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Dự án không tồn tại'
                }), 404
            
            if str(project.owner_id) != current_user['user_id']:
                return jsonify({
                    'success': False,
                    'message': 'Bạn không có quyền sửa dự án này'
                }), 403
            
            update_data = {}
            if 'name' in data:
                update_data['name'] = data['name'].strip()
            if 'description' in data:
                update_data['description'] = data['description'].strip()
            if 'status' in data:
                try:
                    update_data['status'] = ProjectStatus(data['status'])
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Trạng thái không hợp lệ'
                    }), 400
            
            success, message, updated_project = ProjectService.update_project(
                db, project_id, **update_data
            )
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            return jsonify({
                'success': True,
                'message': message,
                'data': ProjectService.project_to_dict(updated_project)
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
    def delete_project(current_user, project_id):
        db = SessionLocal()
        try:
            project = ProjectService.get_project_by_id(db, project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Dự án không tồn tại'
                }), 404
            
            if str(project.owner_id) != current_user['user_id']:
                return jsonify({
                    'success': False,
                    'message': 'Bạn không có quyền xóa dự án này'
                }), 403
            
            success, message = ProjectService.delete_project(db, project_id)
            
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
