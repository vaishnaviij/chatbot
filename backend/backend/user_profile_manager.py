# from datetime import datetime
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
# import config
# from pymongo import MongoClient
# import certifi

# class UserProfileManager:
#     def __init__(self):
#         """Initialize with SSL certificate verification"""
#         self.client = MongoClient(
#             config.MONGO_URI,
#             tls=True,
#             tlsCAFile=certifi.where()
#         )
#         self.db = self.client[config.DATABASE_NAME]
#         self.collection = self.db[config.USER_PROFILES_COLLECTION]    
#     def create_user(self, username, email, password, education_level=None):
#         """Create a new user profile with password authentication."""
#         # Check if user already exists
#         if self.collection.find_one({"$or": [{"username": username}, {"email": email}]}):
#             return False
        
#         # Create new user profile with hashed password
#         user_data = {
#             "username": username,
#             "email": email,
#             "password_hash": generate_password_hash(password),
#             "education_level": education_level,
#             "interests": [],
#             "skills": [],
#             "preferred_careers": [],
#             "conversation_history": [],
#             "created_at": datetime.now(),
#             "last_login": datetime.now()
#         }
        
#         result = self.collection.insert_one(user_data)
#         return result.acknowledged
    
#     def verify_user(self, identifier, password):
#         """Verify user credentials using either email or username."""
#         user = self.collection.find_one({
#             "$or": [
#                 {"email": identifier},
#                 {"username": identifier}
#             ]
#         })
        
#         if user and check_password_hash(user.get("password_hash", ""), password):
#             # Update last login time
#             self.collection.update_one(
#                 {"_id": user["_id"]},
#                 {"$set": {"last_login": datetime.now()}}
#             )
#             # Remove sensitive data before returning
#             user.pop("password_hash", None)
#             return user
#         return None
    
#     def get_user_by_username(self, username):
#         """Get user profile by username."""
#         user = self.collection.find_one({"username": username})
#         if user and '_id' in user:
#             user['_id'] = str(user['_id'])
#         return user
    
#     def get_user_by_id(self, user_id):
#         """Get user by ID with proper error handling"""
#         try:
#             user = self.collection.find_one({"_id": ObjectId(user_id)})
#             if user:
#                 user['_id'] = str(user['_id'])  # Convert ObjectId to string
#             return user
#         except:
#             return None
        
#     def update_user(self, username, updated_data):
#         """Update user profile."""
#         updated_data["last_modified"] = datetime.now()
        
#         result = self.collection.update_one(
#             {"username": username},
#             {"$set": updated_data}
#         )
#         return result.modified_count > 0
    
#     def add_conversation(self, username, conversation):
#         """Add conversation to user's history."""
#         conversation["timestamp"] = datetime.now()
        
#         result = self.collection.update_one(
#             {"username": username},
#             {"$push": {"conversation_history": conversation}}
#         )
#         return result.modified_count > 0
    
#     def get_conversation_history(self, username):
#         """Get conversation history for a user."""
#         user = self.get_user_by_username(username)
#         return user.get("conversation_history", []) if user else None
    
#     def add_interests(self, username, interests):
#         """Add interests to user profile."""
#         result = self.collection.update_one(
#             {"username": username},
#             {"$addToSet": {"interests": {"$each": interests}}}
#         )
#         return result.modified_count > 0
    
#     def add_skills(self, username, skills):
#         """Add skills to user profile."""
#         result = self.collection.update_one(
#             {"username": username},
#             {"$addToSet": {"skills": {"$each": skills}}}
#         )
#         return result.modified_count > 0
    
#     def update_education_level(self, username, education_level):
#         """Update education level in user profile."""
#         return self.update_user(username, {"education_level": education_level})
    
#     def add_preferred_career(self, username, career):
#         """Add preferred career to user profile."""
#         result = self.collection.update_one(
#             {"username": username},
#             {"$addToSet": {"preferred_careers": career}}
#         )
#         return result.modified_count > 0
    
#     def get_all_users(self):
#         """Get all users (for admin purposes)."""
#         users = list(self.collection.find({}))
#         for user in users:
#             user['_id'] = str(user['_id'])
#         return users

#     def delete_user_by_id(self, user_id):
#         """Delete a user by their ID."""
#         result = self.collection.delete_one({"_id": ObjectId(user_id)})
#         return result.deleted_count > 0


from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import config
from pymongo import MongoClient
import certifi

class UserProfileManager:
    def __init__(self):
        """Initialize with SSL certificate verification"""
        self.client = MongoClient(
            config.MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where()
        )
        self.db = self.client[config.DATABASE_NAME]
        self.collection = self.db[config.USER_PROFILES_COLLECTION]    
    def create_user(self, username, email, password, education_level=None):
        """Create a new user profile with password authentication."""
        # Check if user already exists
        if self.collection.find_one({"$or": [{"username": username}, {"email": email}]}):
            return False
        
        # Create new user profile with hashed password
        user_data = {
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(password),
            "education_level": education_level,
            "interests": [],
            "skills": [],
            "preferred_careers": [],
            "conversation_history": [],  # Fixed spelling
            "created_at": datetime.now(),
            "last_login": datetime.now()
        }
        
        result = self.collection.insert_one(user_data)
        return result.acknowledged
    
    def verify_user(self, identifier, password):
        """Verify user credentials using either email or username."""
        user = self.collection.find_one({
            "$or": [
                {"email": identifier},
                {"username": identifier}
            ]
        })
        
        if user and check_password_hash(user.get("password_hash", ""), password):
            # Update last login time
            self.collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.now()}}
            )
            # Remove sensitive data before returning
            user.pop("password_hash", None)
            return user
        return None
    
    def get_user_by_username(self, username):
        """Get user profile by username."""
        user = self.collection.find_one({"username": username})
        if user and '_id' in user:
            user['_id'] = str(user['_id'])
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID with proper error handling"""
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string
            return user
        except:
            return None
        
    def update_user(self, username, updated_data):
        """Update user profile."""
        updated_data["last_modified"] = datetime.now()
        
        result = self.collection.update_one(
            {"username": username},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    
    def add_conversation(self, user_id, conversation):
        """Add conversation to user's history with proper structure."""
        try:
            # First ensure the conversation_history field exists
            self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$setOnInsert": {"conversation_history": []}},
                upsert=True
            )
            
            # Then add the new conversation
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$push": {"conversation_history": conversation},
                    "$set": {"last_modified": datetime.now()}
                }
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")
            return False
    
    def get_conversation_history(self, username):
        """Get conversation history for a user."""
        user = self.get_user_by_username(username)
        return user.get("conversation_history", []) if user else None
    
    def add_interests(self, username, interests):
        """Add interests to user profile."""
        result = self.collection.update_one(
            {"username": username},
            {"$addToSet": {"interests": {"$each": interests}}}
        )
        return result.modified_count > 0
    
    def add_skills(self, username, skills):
        """Add skills to user profile."""
        result = self.collection.update_one(
            {"username": username},
            {"$addToSet": {"skills": {"$each": skills}}}
        )
        return result.modified_count > 0
    
    def update_education_level(self, username, education_level):
        """Update education level in user profile."""
        return self.update_user(username, {"education_level": education_level})
    
    def add_preferred_career(self, username, career):
        """Add preferred career to user profile."""
        result = self.collection.update_one(
            {"username": username},
            {"$addToSet": {"preferred_careers": career}}
        )
        return result.modified_count > 0
    
    def get_all_users(self):
        """Get all users (for admin purposes)."""
        users = list(self.collection.find({}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users

    def delete_user_by_id(self, user_id):
        """Delete a user by their ID."""
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0