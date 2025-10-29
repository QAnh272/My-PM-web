from flask import Blueprint
from apps.controllers.project_controller import ProjectController
from apps.middlewares.auth_middleware import token_required

project_router = Blueprint('project', __name__, url_prefix='/api/projects')


@project_router.route('', methods=['GET'])
@token_required
def get_all_projects(current_user):
    """Get all projects with pagination"""
    return ProjectController.get_all_projects(current_user)


@project_router.route('', methods=['POST'])
@token_required
def create_project(current_user):
    return ProjectController.create_project(current_user)


@project_router.route('/<project_id>', methods=['GET'])
@token_required
def get_project(current_user, project_id):
    return ProjectController.get_project(current_user, project_id)


@project_router.route('/my-projects', methods=['GET'])
@token_required
def get_my_projects(current_user):
    return ProjectController.get_my_projects(current_user)


@project_router.route('/<project_id>', methods=['PUT'])
@token_required
def update_project(current_user, project_id):
    return ProjectController.update_project(current_user, project_id)


@project_router.route('/<project_id>', methods=['DELETE'])
@token_required
def delete_project(current_user, project_id):
    return ProjectController.delete_project(current_user, project_id)
