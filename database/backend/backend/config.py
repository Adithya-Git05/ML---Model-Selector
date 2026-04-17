# Configuration and Constants

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'automl_db')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    
    # Services
    API_GATEWAY_PORT = int(os.getenv('API_GATEWAY_PORT', 5000))
    USER_SERVICE_PORT = int(os.getenv('USER_SERVICE_PORT', 5001))
    AUTH_SERVICE_PORT = int(os.getenv('AUTH_SERVICE_PORT', 5002))
    
    # CORS
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_URI = 'mongodb://localhost:27017'
    DB_NAME = 'automl_db_test'


# Select config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}


# HTTP Status Codes
class HTTPStatus:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


# Custom Error Messages
class ErrorMessages:
    INVALID_EMAIL = "Invalid email format"
    EMAIL_EXISTS = "User with this email already exists"
    WEAK_PASSWORD = "Password does not meet security requirements"
    INVALID_CREDENTIALS = "Invalid email or password"
    TOKEN_MISSING = "Token is missing"
    TOKEN_INVALID = "Invalid or expired token"
    USER_INACTIVE = "User account is inactive"
    USER_NOT_FOUND = "User not found"
    UNAUTHORIZED_ACCESS = "Unauthorized access"
    INTERNAL_ERROR = "Internal server error"


# Success Messages
class SuccessMessages:
    REGISTRATION_SUCCESS = "User registered successfully"
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logged out successfully"
    TOKEN_VALID = "Token is valid"
    TOKEN_REFRESHED = "Token refreshed successfully"
    PROFILE_RETRIEVED = "User profile retrieved successfully"
