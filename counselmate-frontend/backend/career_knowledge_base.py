# # CareerKnowledgeBase.py
# from pymongo import MongoClient, TEXT
# from typing import List, Dict, Any, Optional
# import difflib
# import backend.config as config

# class CareerKnowledgeBase:
#     def __init__(self):
#         """Initialize the Career Knowledge Base with MongoDB connection."""
#         self.client = MongoClient(config.MONGO_URI)
#         self.db = self.client[config.DATABASE_NAME]
#         self.collection = self.db[config.CAREER_DATA_COLLECTION]
        
#         # Create text index for searching
#         self.collection.create_index([("title", TEXT), 
#                                     ("description", TEXT),
#                                     ("required_skills", TEXT),
#                                     ("personality_fit", TEXT),
#                                     ("education_paths", TEXT)])
    
#     def add_career(self, career_data: Dict[str, Any]) -> bool:
#         """Add a new career to the knowledge base.
        
#         Args:
#             career_data: Dictionary with career information
            
#         Returns:
#             bool: True if added successfully, False otherwise
#         """
#         required_fields = ["title", "description", "required_skills"]
        
#         # Check if required fields are present
#         if not all(field in career_data for field in required_fields):
#             return False
        
#         # Check if career already exists
#         if self.collection.find_one({"title": career_data["title"]}):
#             return False
        
#         # Add career
#         result = self.collection.insert_one(career_data)
#         return result.acknowledged
    
#     def get_career(self, title: str) -> Optional[Dict[str, Any]]:
#         """Get career information by title.
        
#         Args:
#             title: Career title to look up
            
#         Returns:
#             Career data dictionary or None if not found
#         """
#         # Try exact match first
#         career = self.collection.find_one({"title": title})
#         if career:
#             return career
        
#         # If no exact match, try fuzzy matching
#         all_careers = self.collection.find({}, {"title": 1})
#         titles = [career["title"] for career in all_careers]
#         matches = difflib.get_close_matches(title, titles, n=1, cutoff=0.6)
        
#         if matches:
#             return self.collection.find_one({"title": matches[0]})
        
#         return None
    
#     def search_by_skills(self, skills: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
#         """Find careers matching given skills.
        
#         Args:
#             skills: List of skills to match
#             top_n: Number of top matches to return
            
#         Returns:
#             List of career data dictionaries
#         """
#         query = {"required_skills": {"$in": skills}}
#         return list(self.collection.find(query).limit(top_n))
    
#     def search_by_interests(self, interests: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
#         """Find careers matching given interests/personality traits.
        
#         Args:
#             interests: List of interests or personality traits
#             top_n: Number of top matches to return
            
#         Returns:
#             List of career data dictionaries
#         """
#         query = {"personality_fit": {"$in": interests}}
#         return list(self.collection.find(query).limit(top_n))
    
#     def search_by_education(self, education_path: str, top_n: int = 5) -> List[Dict[str, Any]]:
#         """Find careers matching a given education path.
        
#         Args:
#             education_path: Education path to match (e.g., "Computer Science degree")
#             top_n: Number of top matches to return
            
#         Returns:
#             List of career data dictionaries
#         """
#         query = {"education_paths": education_path}
#         return list(self.collection.find(query).limit(top_n))
    
#     def text_search(self, search_term: str, top_n: int = 5) -> List[Dict[str, Any]]:
#         """Perform full-text search across career data.
        
#         Args:
#             search_term: Text to search for
#             top_n: Number of top matches to return
            
#         Returns:
#             List of career data dictionaries
#         """
#         return list(self.collection.find(
#             {"$text": {"$search": search_term}},
#             {"score": {"$meta": "textScore"}}
#         ).sort([("score", {"$meta": "textScore"})]).limit(top_n))
    
#     def get_all_careers(self) -> List[Dict[str, Any]]:
#         """Get all careers in the knowledge base."""
#         return list(self.collection.find())
    
#     def get_career_count(self) -> int:
#         """Get the number of careers in the knowledge base."""
#         return self.collection.count_documents({})


from pymongo import MongoClient, TEXT
from typing import List, Dict, Any, Optional
import difflib
import config

class CareerKnowledgeBase:
    def __init__(self):
        """Initialize the Career Knowledge Base with MongoDB connection."""
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DATABASE_NAME]
        self.collection = self.db[config.CAREER_DATA_COLLECTION]
        
        # Check if any text index exists
        existing_indexes = self.collection.index_information()
        text_index_exists = any(
            'text' in index_info.get('weights', {})
            for index_info in existing_indexes.values()
        )
        
        # Create text index only if none exists
        if not text_index_exists:
            try:
                self.collection.create_index([
                    ("title", TEXT), 
                    ("description", TEXT),
                    ("required_skills", TEXT),
                    ("personality_fit", TEXT),
                    ("education_paths", TEXT)
                ], name="career_text_index")
            except Exception as e:
                print(f"Warning: Could not create text index: {str(e)}")
                
    def add_career(self, career_data: Dict[str, Any]) -> bool:
        """Add a new career to the knowledge base."""
        required_fields = ["title", "description", "required_skills"]
        
        if not all(field in career_data for field in required_fields):
            return False
        
        if self.collection.find_one({"title": career_data["title"]}):
            return False
        
        result = self.collection.insert_one(career_data)
        return result.acknowledged
    
    def get_career(self, title: str) -> Optional[Dict[str, Any]]:
        """Get career information by title."""
        career = self.collection.find_one({"title": title})
        if career:
            return career
        
        all_careers = self.collection.find({}, {"title": 1})
        titles = [career["title"] for career in all_careers]
        matches = difflib.get_close_matches(title, titles, n=1, cutoff=0.6)
        
        if matches:
            return self.collection.find_one({"title": matches[0]})
        
        return None
    
    def search_by_skills(self, skills: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
        """Find careers matching given skills."""
        query = {"required_skills": {"$in": skills}}
        return list(self.collection.find(query).limit(top_n))
    
    def search_by_interests(self, interests: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
        """Find careers matching given interests/personality traits."""
        query = {"personality_fit": {"$in": interests}}
        return list(self.collection.find(query).limit(top_n))
    
    def search_by_education(self, education_path: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Find careers matching a given education path."""
        query = {"education_paths": education_path}
        return list(self.collection.find(query).limit(top_n))
    
    def text_search(self, search_term: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Perform full-text search across career data."""
        return list(self.collection.find(
            {"$text": {"$search": search_term}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(top_n))
    
    def get_all_careers(self) -> List[Dict[str, Any]]:
        """Get all careers in the knowledge base."""
        return list(self.collection.find({}, {'_id': 0}))
    
    def get_career_count(self) -> int:
        """Get the number of careers in the knowledge base."""
        return self.collection.count_documents({})
    
    def get_random_careers(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get n random careers from the knowledge base."""
        pipeline = [{'$sample': {'size': n}}]
        return list(self.collection.aggregate(pipeline))