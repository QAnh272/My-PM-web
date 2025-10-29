"""
Comment Routes
"""
from flask import Blueprint
from apps.controllers.comment_controller import CommentController
from apps.middlewares.auth_middleware import token_required

comment_router = Blueprint('comment', __name__, url_prefix='/api/comments')


@comment_router.route('', methods=['POST'])
@token_required
def create_comment(current_user):
    """Create a new comment - Rate limit: 30 per minute"""
    return CommentController.create_comment(current_user)


@comment_router.route('/<comment_id>', methods=['GET'])
@token_required
def get_comment(current_user, comment_id):
    """Get a specific comment by ID"""
    return CommentController.get_comment(current_user, comment_id)


@comment_router.route('/task/<task_id>', methods=['GET'])
@token_required
def get_comments_by_task(current_user, task_id):
    """Get all comments for a task with pagination"""
    return CommentController.get_comments_by_task(current_user, task_id)


@comment_router.route('/my', methods=['GET'])
@token_required
def get_my_comments(current_user):
    """Get all comments by current user"""
    return CommentController.get_my_comments(current_user)


@comment_router.route('/<comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    """Update a comment (author only)"""
    return CommentController.update_comment(current_user, comment_id)


@comment_router.route('/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    """Delete a comment (author only)"""
    return CommentController.delete_comment(current_user, comment_id)


__all__ = ['comment_router']
