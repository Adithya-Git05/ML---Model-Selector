from typing import Optional, List
from bson import ObjectId
from datetime import datetime
from database.connection import db
from models.user import User


class UserRepository:
    """Repository for User database operations"""

    COLLECTION_NAME = "users"

    @staticmethod
    def get_collection():
        """Get users collection"""
        database = db.get_database()
        return database[UserRepository.COLLECTION_NAME]

    @staticmethod
    def create(user: User) -> str:
        """
        Create a new user
        
        Args:
            user: User object
            
        Returns:
            Created user ID
        """
        try:
            collection = UserRepository.get_collection()
            result = collection.insert_one(user.to_dict())
            return str(result.inserted_id)
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")

    @staticmethod
    def find_by_id(user_id: str) -> Optional[User]:
        """
        Find user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        try:
            collection = UserRepository.get_collection()
            user_data = collection.find_one({"_id": ObjectId(user_id)})
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            raise Exception(f"Failed to find user by ID: {str(e)}")

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        """
        Find user by email
        
        Args:
            email: User email
            
        Returns:
            User object or None
        """
        try:
            collection = UserRepository.get_collection()
            user_data = collection.find_one({"email": email.lower()})
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            raise Exception(f"Failed to find user by email: {str(e)}")

    @staticmethod
    def update(user_id: str, user: User) -> bool:
        """
        Update user
        
        Args:
            user_id: User ID
            user: Updated User object
            
        Returns:
            True if update successful
        """
        try:
            collection = UserRepository.get_collection()
            user_data = user.to_dict()
            user_data["updated_at"] = datetime.utcnow()
            result = collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": user_data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Failed to update user: {str(e)}")

    @staticmethod
    def update_last_login(user_id: str) -> bool:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User ID
            
        Returns:
            True if update successful
        """
        try:
            collection = UserRepository.get_collection()
            result = collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Failed to update last login: {str(e)}")

    @staticmethod
    def delete(user_id: str) -> bool:
        """
        Delete user
        
        Args:
            user_id: User ID
            
        Returns:
            True if delete successful
        """
        try:
            collection = UserRepository.get_collection()
            result = collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Failed to delete user: {str(e)}")

    @staticmethod
    def exists_by_email(email: str) -> bool:
        """
        Check if user exists by email
        
        Args:
            email: User email
            
        Returns:
            True if user exists
        """
        try:
            collection = UserRepository.get_collection()
            return collection.find_one({"email": email.lower()}) is not None
        except Exception as e:
            raise Exception(f"Failed to check user existence: {str(e)}")

    @staticmethod
    def get_all() -> List[User]:
        """
        Get all users
        
        Returns:
            List of User objects
        """
        try:
            collection = UserRepository.get_collection()
            users = []
            for user_data in collection.find():
                users.append(User.from_dict(user_data))
            return users
        except Exception as e:
            raise Exception(f"Failed to get all users: {str(e)}")
