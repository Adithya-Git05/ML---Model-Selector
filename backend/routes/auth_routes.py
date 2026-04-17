from flask import Blueprint, request, jsonify
from services.user_service import UserService
from utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePassword123"
    }
    
    Returns:
    {
        "success": true,
        "message": "User registered successfully",
        "user": {...},
        "token": "JWT_TOKEN"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400

        result = UserService.register(
            email=data.get('email'),
            password=data.get('password')
        )

        if not result['success']:
            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePassword123"
    }
    
    Returns:
    {
        "success": true,
        "message": "Login successful",
        "user": {...},
        "token": "JWT_TOKEN"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400

        result = UserService.login(
            email=data.get('email'),
            password=data.get('password')
        )

        if not result['success']:
            return jsonify(result), 401

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Verify JWT token
    
    Request body:
    {
        "token": "JWT_TOKEN"
    }
    
    Returns:
    {
        "success": true,
        "message": "Token is valid",
        "payload": {...}
    }
    """
    try:
        data = request.get_json()
        token = data.get('token') if data else None

        if not token:
            return jsonify({
                "success": False,
                "message": "Token is required"
            }), 400

        result = UserService.verify_token(token)
        status_code = 200 if result['success'] else 401

        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    """
    Refresh JWT token
    
    Request body:
    {
        "token": "JWT_TOKEN"
    }
    
    Returns:
    {
        "success": true,
        "message": "Token refreshed successfully",
        "token": "NEW_JWT_TOKEN"
    }
    """
    try:
        data = request.get_json()
        token = data.get('token') if data else None

        if not token:
            return jsonify({
                "success": False,
                "message": "Token is required"
            }), 400

        result = UserService.refresh_token(token)
        status_code = 200 if result['success'] else 401

        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout user (requires valid token)
    
    Headers:
    Authorization: Bearer JWT_TOKEN
    
    Returns:
    {
        "success": true,
        "message": "Logged out successfully"
    }
    """
    result = UserService.logout(request.user_id)
    return jsonify(result), 200
