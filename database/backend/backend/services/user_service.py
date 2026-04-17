from typing import Dict, Tuple
from email_validator import validate_email, EmailNotValidError
from utils.auth_utils import PasswordHandler, JWTHandler
from models.user import User
from models.user_repository import UserRepository


class UserService:
    """Business logic for user operations"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If email is invalid
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {str(e)}")

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password strength
        
        Args:
            password: Password string
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If password doesn't meet requirements
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        return True

    @staticmethod
    def register(email: str, password: str) -> Dict:
        """
        Register a new user
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Dictionary with user info and token
            
        Raises:
            ValueError: If validation fails
            Exception: If registration fails
        """
        try:
            # Validate inputs
            UserService.validate_email(email)
            UserService.validate_password(password)

            # Check if user already exists
            if UserRepository.exists_by_email(email):
                raise ValueError("User with this email already exists")

            # Hash password
            password_hash = PasswordHandler.hash_password(password)

            # Create user
            user = User(
                email=email.lower(),
                password_hash=password_hash
            )

            user_id = UserRepository.create(user)

            # Generate token
            token = JWTHandler.generate_token(user_id, email.lower(), role="user")

            return {
                "success": True,
                "message": "User registered successfully",
                "user": User.from_dict({"_id": user_id, **user.to_dict()}).to_response(),
                "token": token
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "user": None,
                "token": None
            }
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    @staticmethod
    def login(email: str, password: str) -> Dict:
        """
        Login user
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Dictionary with user info and token
            
        Raises:
            Exception: If login fails
        """
        try:
            # Find user by email
            user = UserRepository.find_by_email(email)
            if not user:
                return {
                    "success": False,
                    "message": "Invalid email or password",
                    "user": None,
                    "token": None
                }

            # Verify password
            if not PasswordHandler.verify_password(password, user.password_hash):
                return {
                    "success": False,
                    "message": "Invalid email or password",
                    "user": None,
                    "token": None
                }

            # Update last login
            UserRepository.update_last_login(user.id)

            # Generate token
            token = JWTHandler.generate_token(user.id, user.email, user.role)

            return {
                "success": True,
                "message": "Login successful",
              Generate token
            token = JWTHandler.generate_token(user.id, user.email, role="user"

    @staticmethod
    def verify_token(token: str) -> Dict:
        """
        Verify JWT token
        
        Args:
            token: JWT token
            
        Returns:
            Dictionary with token verification result
        """
        try:
            payload = JWTHandler.verify_token(token)
            return {
                "success": True,
                "message": "Token is valid",
                "payload": payload
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "payload": None
            }

    @staticmethod
    def refresh_token(token: str) -> Dict:
        """
        Refresh JWT token
        
        Args:
            token: Current JWT token
            
        Returns:
            Dictionary with new token
        """
        try:
            new_token = JWTHandler.refresh_token(token)
            return {
                "success": True,
                "message": "Token refreshed successfully",
                "token": new_token
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "token": None
            }

    @staticmethod
    def get_user(user_id: str) -> Dict:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user info
        """
        try:
            user = UserRepository.find_by_id(user_id)
            if not user:
                return {
                    "success": False,
                    "message": "User not found",
                    "user": None
                }
            return {
                "success": True,
                "message": "User found",
                "user": user.to_response()
            }
        except Exception as e:
            raise Exception(f"Failed to get user: {str(e)}")

    @staticmethod
    def logout(user_id: str) -> Dict:
        """
        Logout user (optional - mainly client-side operation)
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with logout status
        """
        return {
            "success": True,
            "message": "Logged out successfully"
        }
