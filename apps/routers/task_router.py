"""
Task Routes
"""
from flask import Blueprint
from apps.controllers.task_controller import TaskController
from apps.middlewares.auth_middleware import token_required

task_router = Blueprint('task', __name__, url_prefix='/api/tasks')


@task_router.route('', methods=['POST'])
@token_required
def create_task(current_user):
    return TaskController.create_task(current_user)


@task_router.route('/<task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    return TaskController.get_task(current_user, task_id)


@task_router.route('/my', methods=['GET'])
@token_required
def get_my_tasks(current_user):
    return TaskController.get_my_tasks(current_user)


@task_router.route('/project/<project_id>', methods=['GET'])
@token_required
def get_tasks_by_project(current_user, project_id):
    return TaskController.get_tasks_by_project(current_user, project_id)


@task_router.route('/<task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    return TaskController.update_task(current_user, task_id)


@task_router.route('/<task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    return TaskController.delete_task(current_user, task_id)
