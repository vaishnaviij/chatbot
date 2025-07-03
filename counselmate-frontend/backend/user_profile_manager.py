# # UserProfileManager.py
# from datetime import datetime
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import backend.config as config

# class UserProfileManager:
#     def __init__(self):
#         """Initialize the user profile manager with MongoDB connection."""
#         self.client = MongoClient(config.MONGO_URI)
#         self.db = self.client[config.DATABASE_NAME]
#         self.collection = self.db[config.USER_PROFILES_COLLECTION]
    
#     def create_user(self, user_id, name, email=None, education_level=None):
#         """Create a new user profile.
        
#         Args:
#             user_id: Unique identifier for the user
#             name: User's name
#             email: User's email address (optional)
#             education_level: Current education level (optional)
            
#         Returns:
#             bool: True if created successfully, False if user already exists
#         """
#         # Check if user already exists
#         if self.collection.find_one({"user_id": user_id}):
#             return False
        
#         # Create new user profile
#         user_data = {
#             "user_id": user_id,
#             "name": name,
#             "email": email,
#             "education_level": education_level,
#             "interests": [],
#             "skills": [],
#             "preferred_careers": [],
#             "conversation_history": [],
#             "created_at": datetime.now(),
#             "last_login": datetime.now()
#         }
        
#         # Insert user profile
#         result = self.collection.insert_one(user_data)
#         return result.acknowledged
    
#     def get_user(self, user_id):
#         """Get user profile by ID.
        
#         Args:
#             user_id: Unique identifier for the user
            
#         Returns:
#             dict: User profile data or None if not found
#         """
#         return self.collection.find_one({"user_id": user_id})
    
#     def update_user(self, user_id, updated_data):
#         """Update user profile.
        
#         Args:
#             user_id: Unique identifier for the user
#             updated_data: Dictionary of fields to update
            
#         Returns:
#             bool: True if updated successfully, False if user not found
#         """
#         # Add last modified timestamp
#         updated_data["last_modified"] = datetime.now()
        
#         result = self.collection.update_one(
#             {"user_id": user_id},
#             {"$set": updated_data}
#         )
#         return result.modified_count > 0
    
#     def add_conversation(self, user_id, conversation):
#         """Add conversation to user's history.
        
#         Args:
#             user_id: Unique identifier for the user
#             conversation: Dictionary with user and assistant messages
            
#         Returns:
#             bool: True if added successfully, False if user not found
#         """
#         # Add timestamp to conversation
#         conversation["timestamp"] = datetime.now()
        
#         result = self.collection.update_one(
#             {"user_id": user_id},
#             {"$push": {"conversation_history": conversation}}
#         )
#         return result.modified_count > 0
    
#     def get_conversation_history(self, user_id):
#         """Get conversation history for a user.
        
#         Args:
#             user_id: Unique identifier for the user
            
#         Returns:
#             list: List of conversation dictionaries or None if user not found
#         """
#         user = self.get_user(user_id)
#         return user.get("conversation_history", []) if user else None
    
#     def add_interests(self, user_id, interests):
#         """Add interests to user profile.
        
#         Args:
#             user_id: Unique identifier for the user
#             interests: List of interests to add
            
#         Returns:
#             bool: True if added successfully, False if user not found
#         """
#         result = self.collection.update_one(
#             {"user_id": user_id},
#             {"$addToSet": {"interests": {"$each": interests}}}
#         )
#         return result.modified_count > 0
    
#     def add_skills(self, user_id, skills):
#         """Add skills to user profile.
        
#         Args:
#             user_id: Unique identifier for the user
#             skills: List of skills to add
            
#         Returns:
#             bool: True if added successfully, False if user not found
#         """
#         result = self.collection.update_one(
#             {"user_id": user_id},
#             {"$addToSet": {"skills": {"$each": skills}}}
#         )
#         return result.modified_count > 0
    
#     def update_education_level(self, user_id, education_level):
#         """Update education level in user profile.
        
#         Args:
#             user_id: Unique identifier for the user
#             education_level: New education level
            
#         Returns:
#             bool: True if updated successfully, False if user not found
#         """
#         return self.update_user(user_id, {"education_level": education_level})
    
#     def add_preferred_career(self, user_id, career):
#         """Add preferred career to user profile.
        
#         Args:
#             user_id: Unique identifier for the user
#             career: Career title to add
            
#         Returns:
#             bool: True if added successfully, False if user not found
#         """
#         result = self.collection.update_one(
#             {"user_id": user_id},
#             {"$addToSet": {"preferred_careers": career}}
#         )
#         return result.modified_count > 0
    
#     def delete_user(self, user_id):
#         """Delete a user profile.
        
#         Args:
#             user_id: Unique identifier for the user
            
#         Returns:
#             bool: True if deleted successfully, False if user not found
#         """
#         result = self.collection.delete_one({"user_id": user_id})
#         return result.deleted_count > 0
    
#     def get_all_users(self):
#         """Get a list of all user IDs.
        
#         Returns:
#             list: List of user IDs
#         """
#         users = self.collection.find({}, {"user_id": 1})
#         return [user["user_id"] for user in users]

from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import config

class UserProfileManager:
    def __init__(self):
        """Initialize the user profile manager with MongoDB connection."""
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DATABASE_NAME]
        self.collection = self.db[config.USER_PROFILES_COLLECTION]
    
    def create_user(self, user_id, name, email=None, education_level=None):
        """Create a new user profile."""
        if self.collection.find_one({"user_id": user_id}):
            return False
        
        user_data = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "education_level": education_level,
            "interests": [],
            "skills": [],
            "preferred_careers": [],
            "conversation_history": [],
            "created_at": datetime.now(),
            "last_login": datetime.now()
        }
        
        result = self.collection.insert_one(user_data)
        return result.acknowledged
    
    def get_user(self, user_id):
        """Get user profile by ID."""
        user = self.collection.find_one({"user_id": user_id})
        if user and '_id' in user:
            user['_id'] = str(user['_id'])
        return user
    
    def update_user(self, user_id, updated_data):
        """Update user profile."""
        updated_data["last_modified"] = datetime.now()
        
        result = self.collection.update_one(
            {"user_id": user_id},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    
    def add_conversation(self, user_id, conversation):
        """Add conversation to user's history."""
        conversation["timestamp"] = datetime.now()
        
        result = self.collection.update_one(
            {"user_id": user_id},
            {"$push": {"conversation_history": conversation}}
        )
        return result.modified_count > 0
    
    def get_conversation_history(self, user_id):
        """Get conversation history for a user."""
        user = self.get_user(user_id)
        return user.get("conversation_history", []) if user else None
    
    def add_interests(self, user_id, interests):
        """Add interests to user profile."""
        result = self.collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"interests": {"$each": interests}}}
        )
        return result.modified_count > 0
    
    def add_skills(self, user_id, skills):
        """Add skills to user profile."""
        result = self.collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"skills": {"$each": skills}}}
        )
        return result.modified_count > 0
    
    def update_education_level(self, user_id, education_level):
        """Update education level in user profile."""
        return self.update_user(user_id, {"education_level": education_level})
    
    def add_preferred_career(self, user_id, career):
        """Add preferred career to user profile."""
        result = self.collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"preferred_careers": career}}
        )
        return result.modified_count > 0
    
    def delete_user(self, user_id):
        """Delete a user profile."""
        result = self.collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0
    
    def get_all_users(self):
        """Get a list of all user IDs."""
        users = self.collection.find({}, {"user_id": 1, "_id": 0})
        return [user["user_id"] for user in users]