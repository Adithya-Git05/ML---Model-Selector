import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database.connection import db
from utils.auth_utils import JWTHandler, token_required
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Enable CORS
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    """Initialize database before each request"""
    if db.db is None:
        db.connect()


@app.teardown_appcontext
def teardown_db(exception=None):
    """Close database connection after each request"""
    pass


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "API Gateway"
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('API_GATEWAY_PORT', 5000))
    try:
        db.connect()
        print(f"✓ Starting API Gateway on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"✗ Failed to start server: {str(e)}")
    finally:
        db.close()
