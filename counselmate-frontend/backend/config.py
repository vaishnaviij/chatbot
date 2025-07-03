


import os
from dotenv import load_dotenv

load_dotenv()

# API configuration
API_TOKEN = os.getenv("HF_API_TOKEN", "your_hf_token")
API_URL = os.getenv("HF_API_URL", "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2")

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "your_mongo_url")
DATABASE_NAME = os.getenv("DATABASE_NAME", "counselmate")
USER_PROFILES_COLLECTION = os.getenv("USER_PROFILES_COLLECTION", "user_profiles")
CAREER_DATA_COLLECTION = os.getenv("CAREER_DATA_COLLECTION", "career_data")

# System prompt for the career counseling chatbot
SYSTEM_PROMPT = """You are Counselmate, an AI career counselor designed to help students with career guidance. 
Your role is to:
1. Ask relevant questions about the student's interests, skills, and academic background
2. Provide personalized career recommendations based on their responses
3. Offer information about potential career paths, required education, and job prospects
4. Help students explore their options without pushing them in any specific direction
5. Provide encouragement and support throughout their career exploration journey

Be empathetic, informative, and focused on helping students make informed career decisions.

IMPORTANT: Respond ONLY to the user's most recent message. Do not make up a conversation or generate both user and assistant messages."""

# Flask configuration
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your-secret-key-here")
