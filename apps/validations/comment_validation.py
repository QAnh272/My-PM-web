from flask import request, jsonify


def validate_create_comment():
    """Validate comment creation data."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    content = data.get('content', '').strip()
    task_id = data.get('task_id', '').strip()
    
    if not content:
        return jsonify({"error": "Content is required"}), 400
    
    if len(content) < 1:
        return jsonify({"error": "Content cannot be empty"}), 400
    
    if len(content) > 5000:
        return jsonify({"error": "Content is too long (max 5000 characters)"}), 400
    
    if not task_id:
        return jsonify({"error": "Task ID is required"}), 400
    
    return None


def validate_update_comment():
    """Validate comment update data."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    content = data.get('content')
    
    if content is None:
        return jsonify({"error": "Content is required"}), 400
    
    content = content.strip()
    
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400
    
    if len(content) < 1:
        return jsonify({"error": "Content must have at least 1 character"}), 400
    
    if len(content) > 5000:
        return jsonify({"error": "Content is too long (max 5000 characters)"}), 400
    
    return None


def validate_comment_id(comment_id):
    """Validate comment ID format."""
    if not comment_id:
        return jsonify({"error": "Comment ID is required"}), 400
    
    try:
        from uuid import UUID
        UUID(str(comment_id))
    except ValueError:
        return jsonify({"error": "Invalid comment ID format"}), 400
    
    return None


__all__ = ['validate_create_comment', 'validate_update_comment', 'validate_comment_id']
