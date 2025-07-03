from admin_manager import AdminManager
from config import MONGO_URI, DATABASE_NAME, ADMIN_DATA_COLLECTION

if __name__ == "__main__":
    admin_manager = AdminManager()
    
    # Create initial super admin
    admin_manager.create_admin(
        username="admin",
        email="admin@gmail.com",
        password="123456"
    )
    
    # Grant super admin privileges
    admin_manager.grant_super_admin("superadmin")
    
    print("Initial super admin created successfully")