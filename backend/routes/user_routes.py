from flask import Blueprint, request, jsonify
from services.user_service import UserService
from app import token_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.route('/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """
    Get user profile (requires valid token)
    
    Parameters:
    user_id: User ID (path parameter)
    
    Headers:
    Authorization: Bearer JWT_TOKEN
    
    Returns:
    {
        "success": true,
        "message": "User found",
        "user": {...}
    }
    """
    try:
        # Optional: Check if user is getting their own profile or is admin
        if request.user_id != user_id:
            return jsonify({
                "success": False,
                "message": "Unauthorized access"
            }), 403

        result = UserService.get_user(user_id)

        if not result['success']:
            return jsonify(result), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """
    Get current user profile (requires valid token)
    
    Headers:
    Authorization: Bearer JWT_TOKEN
    
    Returns:
    {
        "success": true,
        "message": "User found",
        "user": {...}
    }
    """
    try:
        result = UserService.get_user(request.user_id)

        if not result['success']:
            return jsonify(result), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
