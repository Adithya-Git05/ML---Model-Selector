import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class JWTHandler:
    """Handle JWT token generation and validation"""
    
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 24))

    @staticmethod
    def generate_token(user_id: str, email: str, role: str = "user") -> str:
        """
        Generate JWT token for user
        
        Args:
            user_id: MongoDB ObjectId as string
            email: User email
            role: User role (default: "user")
            
        Returns:
            JWT token string
        """
        try:
            payload = {
                "user_id": str(user_id),
                "email": email,
                "role": role,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(hours=JWTHandler.EXPIRATION_HOURS)
            }
            token = jwt.encode(payload, JWTHandler.SECRET_KEY, algorithm=JWTHandler.ALGORITHM)
            return token
        except Exception as e:
            raise Exception(f"Token generation failed: {str(e)}")

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            jwt.ExpiredSignatureError: Token has expired
            jwt.InvalidTokenError: Token is invalid
        """
        try:
            payload = jwt.decode(token, JWTHandler.SECRET_KEY, algorithms=[JWTHandler.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    @staticmethod
    def refresh_token(token: str) -> str:
        """
        Refresh an existing token
        
        Args:
            token: Current JWT token
            
        Returns:
            New JWT token
        """
        try:
            payload = JWTHandler.verify_token(token)
            return JWTHandler.generate_token(payload["user_id"], payload["email"], payload["role"])
        except Exception as e:
            raise Exception(f"Token refresh failed: {str(e)}")


class PasswordHandler:
    """Handle password hashing and verification"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        try:
            salt = bcrypt.gensalt(rounds=10)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            raise Exception(f"Password hashing failed: {str(e)}")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            raise Exception(f"Password verification failed: {str(e)}")
