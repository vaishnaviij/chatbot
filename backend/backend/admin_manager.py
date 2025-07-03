from pymongo import MongoClient
import certifi
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import config

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import certifi

class AdminManager:
    def __init__(self):
        self.client = MongoClient(
            config.MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where()
        )
        self.db = self.client[config.DATABASE_NAME]
        self.collection = self.db[config.ADMIN_DATA_COLLECTION]
    
    def get_all_admins(self):
        """Get all admin users with basic info"""
        try:
            admins = list(self.collection.find(
                {},
                {
                    '_id': 1,
                    'username': 1,
                    'email': 1,
                    'created_at': 1,
                    'is_super_admin': 1,
                    'last_login': 1
                }
            ))
            # Convert ObjectId to string
            for admin in admins:
                admin['_id'] = str(admin['_id'])
            return admins
        except Exception as e:
            print(f"Error getting admins: {str(e)}")
            return []
            
    def create_admin(self, username, email, password):
        """Create a new admin account"""
        # Check if admin already exists
        if self.collection.find_one({"$or": [{"username": username}, {"email": email}]}):
            return False
        
        # Create new admin
        admin_data = {
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(password),
            "created_at": datetime.now(),
            "last_login": None,
            "permissions": ["manage_users", "manage_careers", "view_analytics"],
            "is_super_admin": False
        }
        
        result = self.collection.insert_one(admin_data)
        return result.acknowledged
    
    def verify_admin(self, username, password):
        """Verify admin credentials with better error handling"""
        try:
            admin = self.collection.find_one({"username": username})
            
            if not admin:
                print(f"Admin not found: {username}")
                return None
                
            if not check_password_hash(admin.get("password_hash", ""), password):
                print("Password mismatch for admin:", username)
                return None
                
            # Update last login time
            self.collection.update_one(
                {"_id": admin["_id"]},
                {"$set": {"last_login": datetime.now()}}
            )
            # Remove sensitive data before returning
            admin.pop("password_hash", None)
            return admin
            
        except Exception as e:
            print(f"Error verifying admin: {str(e)}")
            return None
        
    def get_admin_by_id(self, admin_id):
        """Get admin by ID with proper error handling"""
        try:
            admin = self.collection.find_one({"_id": ObjectId(admin_id)})
            if admin:
                admin.pop("password_hash", None)
                admin['_id'] = str(admin['_id'])  # Convert ObjectId to string
            return admin
        except:
            return None

    def get_admin_by_username(self, username):
        """Get admin by username with proper error handling"""
        try:
            admin = self.collection.find_one({"username": username})
            if admin:
                admin.pop("password_hash", None)
                admin['_id'] = str(admin['_id'])  # Convert ObjectId to string
            return admin
        except:
            return None    
    def update_admin(self, username, updated_data):
        """Update admin profile"""
        updated_data["last_modified"] = datetime.now()
        
        result = self.collection.update_one(
            {"username": username},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    
    def delete_admin(self, username):
        """Delete an admin account"""
        result = self.collection.delete_one({"username": username})
        return result.deleted_count > 0
        
    def grant_super_admin(self, username):
        """Grant super admin privileges"""
        result = self.collection.update_one(
            {"username": username},
            {"$set": {"is_super_admin": True}}
        )
        return result.modified_count > 0