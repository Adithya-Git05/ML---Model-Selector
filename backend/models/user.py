from datetime import datetime
from typing import Optional, Dict
from bson import ObjectId


class User:
    """User model"""
    
    def __init__(self, email: str, password_hash: str, id: Optional[str] = None):
        self.id = id or str(ObjectId())
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            "_id": ObjectId(self.id) if isinstance(self.id, str) else self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_response(self) -> Dict:
        """Convert user to API response (exclude sensitive data)"""
        return {
            "id": str(self.id),
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """Create User object from dictionary"""
        user = User(
            email=data.get("email"),
            password_hash=data.get("password_hash"),
            id=str(data["_id"]) if "_id" in data else None
        )
        user.created_at = data.get("created_at", datetime.utcnow())
        user.updated_at = data.get("updated_at", datetime.utcnow())
        return user
