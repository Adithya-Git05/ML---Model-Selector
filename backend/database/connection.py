import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def connect(self):
        """Connect to MongoDB"""
        try:
            mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            self.client = MongoClient(mongodb_uri)
            db_name = os.getenv("DB_NAME", "automl_db")
            self.db = self.client[db_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"✓ Connected to MongoDB database: {db_name}")
            return self.db
        except Exception as e:
            print(f"✗ Failed to connect to MongoDB: {str(e)}")
            raise

    def get_database(self):
        """Get database instance"""
        if self.db is None:
            self.connect()
        return self.db

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")


# Singleton instance
db = MongoDBConnection()
