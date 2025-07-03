from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId
import os
import re
import json
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from career_knowledge_base import CareerKnowledgeBase
from user_profile_manager import UserProfileManager
from admin_manager import AdminManager
import config
from functools import wraps


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

try:
    kb = CareerKnowledgeBase()
    user_manager = UserProfileManager()
    admin_manager = AdminManager()
except Exception as e:
    print(f"Failed to initialize database connections: {e}")

# Headers for API request
headers = {
    "Authorization": f"Bearer {config.API_TOKEN}",
    "Content-Type": "application/json"
}

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for admin_username in both GET params and POST body
        admin_username = None
        if request.method == 'GET':
            admin_username = request.args.get('admin_username')
        else:
            if request.is_json:
                data = request.get_json()
                admin_username = data.get('admin_username')
            else:
                admin_username = request.form.get('admin_username')
        
        if not admin_username:
            return jsonify({"success": False, "message": "Admin username required"}), 400
        
        # Check both collections for admin
        admin = admin_manager.get_admin_by_username(admin_username)
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
        
        # Verify admin status in user collection too
        user_admin = user_manager.get_user_by_username(admin_username)
        if not user_admin or not user_admin.get('is_admin', False):
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        
        # Store admin info in request context for later use
        request.admin = admin
        return f(*args, **kwargs)
    return decorated_function

def extract_career_interests(text):
    """Extract potential career interests from user input."""
    interests = []
    skills = []
    
    interest_keywords = ["creative", "analytical", "helping people", "working with animals", 
                        "technology", "science", "art", "business", "teaching", "healthcare",
                        "building", "designing", "communicating", "writing", "problem-solving"]
    
    skill_keywords = ["programming", "writing", "math", "communication", "leadership",
                    "organization", "creativity", "analysis", "research", "design",
                    "languages", "teaching", "problem-solving", "teamwork"]
    
    for keyword in interest_keywords:
        if keyword.lower() in text.lower():
            interests.append(keyword)
    
    for keyword in skill_keywords:
        if keyword.lower() in text.lower():
            skills.append(keyword)
    
    return interests, skills

def extract_education_info(text):
    """Extract education information from user input."""
    education = []
    
    education_patterns = [
        r"high school", r"bachelor'?s degree", r"master'?s degree", r"phd", r"doctorate",
        r"associate'?s degree", r"college", r"university", r"vocational", r"diploma",
        r"certificate", r"bootcamp", r"studying ([a-zA-Z\s]+)"
    ]
    
    for pattern in education_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            if pattern == r"studying ([a-zA-Z\s]+)" and matches[0]:
                education.append(f"studying {matches[0]}")
            else:
                education.append(re.sub(r'[^a-zA-Z\s]', '', pattern))
    
    return education

def enrich_response_with_knowledge(user_input, model_response, user_id=None):
    """Enrich the model's response with knowledge base information."""
    interests, skills = extract_career_interests(user_input)
    education = extract_education_info(user_input)
    
    if user_id:
        if interests:
            user_manager.add_interests(user_id, interests)
        if skills:
            user_manager.add_skills(user_id, skills)
        if education and len(education) > 0:
            user_manager.update_education_level(user_id, education[0])
    
    career_recommendations = []
    
    if interests and skills:
        skill_based = kb.search_by_skills(skills, top_n=3)
        interest_based = kb.search_by_interests(interests, top_n=3)
        
        seen_titles = set()
        for career in skill_based + interest_based:
            if career["title"] not in seen_titles:
                career_recommendations.append(career)
                seen_titles.add(career["title"])
    elif interests:
        career_recommendations = kb.search_by_interests(interests, top_n=3)
    elif skills:
        career_recommendations = kb.search_by_skills(skills, top_n=3)
    elif education:
        for edu in education:
            edu_recommendations = kb.search_by_education(edu, top_n=2)
            career_recommendations.extend(edu_recommendations)
    
    if career_recommendations:
        career_info = "\n\nBased on what you've shared, here are some career paths you might consider:\n\n"
        
        for i, career in enumerate(career_recommendations[:3], 1):
            career_info += f"{i}. {career['title']}:\n"
            career_info += f"   - {career['description']}\n"
            career_info += f"   - Required skills: {', '.join(career['required_skills'][:3])}\n"
            career_info += f"   - Education paths: {', '.join(career['education_paths'][:2])}\n"
            career_info += f"   - Salary range: {career['avg_salary_range']['entry']} - {career['avg_salary_range']['senior']}\n"
            
            if i < len(career_recommendations[:3]):
                career_info += "\n"
        
        career_keywords = ["career", "job", "profession", "occupation", "work", "field"]
        if any(keyword in user_input.lower() for keyword in career_keywords) or \
           any(keyword in model_response.lower() for keyword in career_keywords):
            return model_response + career_info
    
    return model_response

def create_prompt(conversation_history):
    # Start with system prompt
    prompt = config.SYSTEM_PROMPT + "\n\n"
    
    # Only include the most recent user message
    if conversation_history:
        last_user_message = next(
            (msg for msg in reversed(conversation_history) if msg["role"] == "user"),
            None
        )
        if last_user_message:
            prompt += f"User: {last_user_message['content']}\nAssistant: "
    
    return prompt

def query_model(conversation_history):
    prompt = create_prompt(conversation_history)
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(config.API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "").strip()
                return validate_response(generated_text)
            return validate_response(str(result))
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "I'm sorry, I encountered an error while processing your career question."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "I'm sorry, I encountered an error while processing your career question."

def validate_response(response):
    # Check if response is generating user messages
    if response.startswith("User:") or "User:" in response:
        return "I'm sorry, I encountered an error. Please try asking your career question again."
    
    # Check if response is non-career related
    career_keywords = ["career", "job", "skill", "education", "profession", 
                      "salary", "industry", "position", "degree"]
    if not any(keyword.lower() in response.lower() for keyword in career_keywords):
        return ("I'm Counselmate, your career guidance assistant. I specialize in career-related questions "
                "about education paths, skills, jobs, or professions. What career questions can I help you with?")
    
    return response
 
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    education_level = data.get('education_level', None)
    
    if not all([username, email, password]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    if user_manager.create_user(username, email, password, education_level):
        return jsonify({
            "success": True,
            "message": "User registered successfully"
        })
    return jsonify({
        "success": False,
        "message": "Username or email already exists"
    }), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('identifier')  # Can be email or username
    password = data.get('password')
    
    if not all([identifier, password]):
        return jsonify({"success": False, "message": "Missing credentials"}), 400
    
    user = user_manager.verify_user(identifier, password)
    if user:
        # Convert ObjectId to string for JSON serialization
        user['_id'] = str(user['_id'])
        return jsonify({
            "success": True,
            "user": user
        })
    return jsonify({
        "success": False,
        "message": "Invalid credentials"
    }), 401

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print("Received chat request with data:", data)  # Debug log
    
    if not data or 'message' not in data:
        return jsonify({"success": False, "message": "Message is required"}), 400

    user_id = data.get('user_id')
    message = data.get('message')
    conversation_history = data.get('conversation_history', [])

    try:
        print(f"Processing message for user {user_id}")  # Debug log
        response, updated_history = process_user_message(user_id, message, conversation_history)
        return jsonify({
            'success': True,
            'response': response,
            'conversation_history': updated_history
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # Debug log
        return jsonify({"success": False, "message": str(e)}), 500

def process_user_message(user_id, message, conversation_history=None):
    try:
        user_manager = UserProfileManager()
        
        # Get existing conversation history if not provided
        if conversation_history is None:
            if user_id != 'anonymous':
                user_data = user_manager.get_user_by_id(user_id)
                if user_data:
                    # Check both spellings of the field
                    conversation_history = user_data.get("conversation_history", 
                                                      user_data.get("conversation_nistory", []))
                else:
                    conversation_history = []
            else:
                conversation_history = []
                
        # Add new user message
        user_message = {"role": "user", "content": message}
        model_messages = conversation_history[-10:] + [user_message]  # Keep last 10 messages
        
        # Get response from model
        response = query_model(model_messages)
        
        # Save to database if not anonymous user
        if user_id != 'anonymous':
            save_data = {
                "user": message,
                "assistant": response,
                "timestamp": datetime.now()
            }
            
            # Ensure the conversation_history field exists
            user_manager.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$setOnInsert": {"conversation_history": []}},
                upsert=True
            )
            
            # Add new conversation
            user_manager.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"conversation_history": save_data}}
            )

        return response, conversation_history + [user_message, {"role": "assistant", "content": response}]
        
    except Exception as e:
        print(f"Error in process_user_message: {str(e)}")
        raise e

@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    try:
        # Remove fields that shouldn't be updated directly
        data.pop('_id', None)
        data.pop('password_hash', None)
        data.pop('created_at', None)
        
        # Convert comma-separated strings to arrays if needed
        if 'interests' in data and isinstance(data['interests'], str):
            data['interests'] = [i.strip() for i in data['interests'].split(',') if i.strip()]
        
        if 'skills' in data and isinstance(data['skills'], str):
            data['skills'] = [s.strip() for s in data['skills'].split(',') if s.strip()]
        
        data['last_modified'] = datetime.now()
        
        # Update using user_id instead of username
        result = user_manager.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "User updated successfully"})
        return jsonify({"success": False, "message": "User update failed"}), 400
        
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
        
@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    user_data = user_manager.get_user_by_username(username)
    if user_data:
        # Remove sensitive data before returning
        user_data.pop('password_hash', None)
        user_data.pop('_id', None)
        return jsonify({
            'success': True,
            'user': user_data
        })
    return jsonify({
        'success': False,
        'message': 'User not found'
    }), 404

@app.route('/api/careers/suggest', methods=['POST'])
def suggest_careers():
    data = request.get_json()
    print("Received suggestion request with data:", data)  # Debug log
    
    interests = data.get('interests', [])
    skills = data.get('skills', [])
    education = data.get('education', None)
    
    print(f"Searching with interests: {interests}, skills: {skills}, education: {education}")  # Debug log
    
    careers = []
    
    if interests and skills:
        print("Searching by both interests and skills")  # Debug log
        skill_based = kb.search_by_skills(skills, top_n=5)
        interest_based = kb.search_by_interests(interests, top_n=5)
        careers = skill_based + interest_based
    elif interests:
        print("Searching by interests only")  # Debug log
        careers = kb.search_by_interests(interests, top_n=5)
    elif skills:
        print("Searching by skills only")  # Debug log
        careers = kb.search_by_skills(skills, top_n=5)
    elif education:
        print("Searching by education only")  # Debug log
        careers = kb.search_by_education(education, top_n=5)
    
    print(f"Found {len(careers)} careers")  # Debug log
    
    # Remove duplicates and convert ObjectIds to strings
    seen = set()
    unique_careers = []
    for career in careers:
        if career['title'] not in seen:
            seen.add(career['title'])
            # Convert ObjectId to string
            career['_id'] = str(career['_id'])
            unique_careers.append(career)
    
    return jsonify({
        'success': True,
        'careers': unique_careers[:5]
    })
    
# Admin Management Routes
@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    try:
        admin_username = request.args.get('admin_username')
        admin = admin_manager.get_admin_by_username(admin_username)
        
        if not admin:
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        users = user_manager.get_all_users()
        # Ensure all users have required fields
        safe_users = []
        for user in users:
            safe_users.append({
                '_id': str(user.get('_id', '')),
                'username': user.get('username', ''),
                'email': user.get('email', ''),
                'created_at': user.get('created_at', datetime.utcnow()),
                'is_admin': user.get('is_admin', False)
            })
        
        return jsonify({"success": True, "users": safe_users})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/make-admin', methods=['POST'])
def make_user_admin():
    try:
        data = request.get_json()
        admin_username = data.get('admin_username')
        user_id = data.get('user_id')
        
        admin = admin_manager.get_admin_by_username(admin_username)
        if not admin or not admin.get('is_super_admin', False):
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        # First check if user exists
        user = user_manager.get_user_by_id(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Promote user to admin
        result = user_manager.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_admin": True}}
        )
        
        if result.modified_count == 0:
            return jsonify({"success": False, "message": "User not found"}), 404
            
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        # Get requester from request context (set by decorator)
        requester = request.admin
        
        # Get target user
        target_user = user_manager.get_user_by_id(user_id)
        if not target_user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Check if target is an admin
        if target_user.get('is_admin', False):
            # Only super admins can delete other admins
            if not requester.get('is_super_admin', False):
                return jsonify({"success": False, "message": "Only super admins can delete other admins"}), 403

            # Also remove from admin collection if exists
            admin_manager.collection.delete_one({"username": target_user['username']})

        # Delete from user collection
        user_manager.collection.delete_one({"_id": ObjectId(user_id)})
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
            
@app.route('/api/admin/auth/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    requester_username = data.get('requester_username')
    
    if not all([username, email, password, requester_username]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    # Verify requesting user is a super admin
    requester = admin_manager.get_admin_by_username(requester_username)
    if not requester or not requester.get('is_super_admin', False):
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    # Check if username or email already exists
    if admin_manager.get_admin_by_username(username) or admin_manager.get_admin_by_email(email):
        return jsonify({"success": False, "message": "Username or email already exists"}), 400

    # Create in both collections
    admin_data = {
        "username": username,
        "email": email,
        "password_hash": generate_password_hash(password),
        "is_super_admin": False,
        "created_at": datetime.now(),
        "last_login": None
    }
    
    # Add to admin collection
    admin_manager.collection.insert_one(admin_data)
    
    # Add to user collection as admin
    user_manager.collection.insert_one({
        **admin_data,
        "is_admin": True
    })
    
    return jsonify({"success": True})

@app.route('/api/admin/auth/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({"success": False, "message": "Missing credentials"}), 400
    
    try:
        admin = admin_manager.verify_admin(username, password)
        if admin:
            # Convert ObjectId to string for JSON serialization
            admin['_id'] = str(admin['_id'])
            return jsonify({
                "success": True,
                "admin": admin
            })
        return jsonify({
            "success": False,
            "message": "Invalid admin credentials"
        }), 401
    except Exception as e:
        print(f"Admin login error: {str(e)}")  # Add this logging
        return jsonify({
            "success": False,
            "message": "An error occurred. Please try again."
        }), 500
    
@app.route('/api/admin/list', methods=['GET'])
def list_admins():
    username = request.args.get('username')
    
    # Verify requesting user is an admin
    requester = admin_manager.get_admin_by_username(username)
    if not requester:
        return jsonify({"success": False, "message": "Admin privileges required"}), 403
    
    admins = admin_manager.get_all_admins()
    return jsonify({
        "success": True,
        "admins": admins
    })

@app.route('/api/admin/grant-super', methods=['POST'])
def grant_super_admin():
    data = request.get_json()
    target_username = data.get('target_username')
    requester_username = data.get('requester_username')
    
    # Verify requesting user is a super admin
    requester = admin_manager.get_admin_by_username(requester_username)
    if not requester or not requester.get('is_super_admin', False):
        return jsonify({"success": False, "message": "Super admin privileges required"}), 403
    
    if admin_manager.grant_super_admin(target_username):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Admin not found"}), 404
# Admin Career Management
@app.route('/api/admin/careers', methods=['GET'])
def get_all_careers():
    try:
        admin_username = request.args.get('admin_username')
        admin = admin_manager.get_admin_by_username(admin_username)
        
        if not admin:
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        careers = list(kb.collection.find({}))
        for career in careers:
            career['_id'] = str(career['_id'])
        return jsonify({"success": True, "careers": careers})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Admin Management
@app.route('/api/admin/admins', methods=['GET'])
def get_all_admins():
    try:
        admin_username = request.args.get('admin_username')
        requesting_admin = admin_manager.get_admin_by_username(admin_username)
        
        # Verify requesting user is a super admin
        if not requesting_admin or not requesting_admin.get('is_super_admin', False):
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        admins = admin_manager.get_all_admins()
        return jsonify({
            "success": True,
            "admins": admins
        })
    except Exception as e:
        print(f"Error in /api/admin/admins: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch admins",
            "error": str(e)
        }), 500
                
@app.route('/api/admin/demote-admin', methods=['POST'])
@admin_required
def demote_admin():
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        
        # Get requester from request context (set by decorator)
        requester = request.admin
        
        # Verify requester is super admin
        if not requester.get('is_super_admin', False):
            return jsonify({"success": False, "message": "Super admin privileges required"}), 403

        # Cannot demote yourself
        target_admin = admin_manager.get_admin_by_id(admin_id)
        if not target_admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
            
        if str(target_admin['_id']) == str(requester['_id']):
            return jsonify({"success": False, "message": "Cannot demote yourself"}), 400

        # Update in user collection
        user_manager.collection.update_one(
            {"username": target_admin['username']},
            {"$set": {"is_admin": False}}
        )
        
        # Remove from admin collection
        admin_manager.collection.delete_one({"_id": ObjectId(admin_id)})
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)