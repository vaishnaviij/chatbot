# # app.py
# import os
# import re
# import json
# import uuid
# import requests
# from backend.career_knowledge_base import CareerKnowledgeBase
# from backend.user_profile_manager import UserProfileManager
# import backend.config as config

# kb = CareerKnowledgeBase()
# user_manager = UserProfileManager()

# # Headers for API request
# headers = {
#     "Authorization": f"Bearer {config.API_TOKEN}",
#     "Content-Type": "application/json"
# }

# def extract_career_interests(text):
#     """Extract potential career interests from user input."""
#     # Simple keyword extraction - could be enhanced with more sophisticated NLP
#     interests = []
#     skills = []
    
#     # Common interest keywords
#     interest_keywords = ["creative", "analytical", "helping people", "working with animals", 
#                         "technology", "science", "art", "business", "teaching", "healthcare",
#                         "building", "designing", "communicating", "writing", "problem-solving"]
    
#     # Common skill keywords  
#     skill_keywords = ["programming", "writing", "math", "communication", "leadership",
#                     "organization", "creativity", "analysis", "research", "design",
#                     "languages", "teaching", "problem-solving", "teamwork"]
    
#     # Check for interests
#     for keyword in interest_keywords:
#         if keyword.lower() in text.lower():
#             interests.append(keyword)
    
#     # Check for skills
#     for keyword in skill_keywords:
#         if keyword.lower() in text.lower():
#             skills.append(keyword)
    
#     return interests, skills

# def extract_education_info(text):
#     """Extract education information from user input."""
#     education = []
    
#     # Education level patterns
#     education_patterns = [
#         r"high school", r"bachelor'?s degree", r"master'?s degree", r"phd", r"doctorate",
#         r"associate'?s degree", r"college", r"university", r"vocational", r"diploma",
#         r"certificate", r"bootcamp", r"studying ([a-zA-Z\s]+)"
#     ]
    
#     # Check for education info
#     for pattern in education_patterns:
#         matches = re.findall(pattern, text.lower())
#         if matches:
#             if pattern == r"studying ([a-zA-Z\s]+)" and matches[0]:
#                 education.append(f"studying {matches[0]}")
#             else:
#                 education.append(re.sub(r'[^a-zA-Z\s]', '', pattern))
    
#     return education

# def enrich_response_with_knowledge(user_input, model_response, user_id=None):
#     """Enrich the model's response with knowledge base information."""
#     # Extract interests and skills from user input
#     interests, skills = extract_career_interests(user_input)
#     education = extract_education_info(user_input)
    
#     # Update user profile if available
#     if user_id:
#         if interests:
#             user_manager.add_interests(user_id, interests)
#         if skills:
#             user_manager.add_skills(user_id, skills)
#         if education and len(education) > 0:
#             user_manager.update_education_level(user_id, education[0])
    
#     # Get career recommendations based on extracted information
#     career_recommendations = []
    
#     # Check if we have enough information to make recommendations
#     if interests and skills:
#         # Get recommendations based on interests and skills
#         skill_based = kb.search_by_skills(skills, top_n=3)
#         interest_based = kb.search_by_interests(interests, top_n=3)
        
#         # Combine recommendations (remove duplicates)
#         seen_titles = set()
#         for career in skill_based + interest_based:
#             if career["title"] not in seen_titles:
#                 career_recommendations.append(career)
#                 seen_titles.add(career["title"])
#     elif interests:
#         career_recommendations = kb.search_by_interests(interests, top_n=3)
#     elif skills:
#         career_recommendations = kb.search_by_skills(skills, top_n=3)
#     elif education:
#         for edu in education:
#             edu_recommendations = kb.search_by_education(edu, top_n=2)
#             career_recommendations.extend(edu_recommendations)
    
#     # If we have recommendations, enhance the response
#     if career_recommendations:
#         # Create a career information section
#         career_info = "\n\nBased on what you've shared, here are some career paths you might consider:\n\n"
        
#         for i, career in enumerate(career_recommendations[:3], 1):
#             career_info += f"{i}. {career['title']}:\n"
#             career_info += f"   - {career['description']}\n"
#             career_info += f"   - Required skills: {', '.join(career['required_skills'][:3])}\n"
#             career_info += f"   - Education paths: {', '.join(career['education_paths'][:2])}\n"
#             career_info += f"   - Salary range: {career['avg_salary_range']['entry']} - {career['avg_salary_range']['senior']}\n"
            
#             if i < len(career_recommendations[:3]):
#                 career_info += "\n"
        
#         # Add the career info to the response, but only if it seems relevant
#         career_keywords = ["career", "job", "profession", "occupation", "work", "field"]
#         if any(keyword in user_input.lower() for keyword in career_keywords) or \
#            any(keyword in model_response.lower() for keyword in career_keywords):
#             return model_response + career_info
    
#     return model_response

# def create_prompt(conversation_history):
#     """Create a simple text prompt from the conversation history"""
#     prompt = config.SYSTEM_PROMPT + "\n\n"
    
#     for message in conversation_history:
#         role = message["role"]
#         content = message["content"]
        
#         if role == "user":
#             prompt += f"User: {content}\n"
#         else:  # assistant
#             prompt += f"Counselmate: {content}\n"
    
#     # Add the final prompt for the assistant to respond
#     prompt += "Counselmate: "
#     return prompt

# def query_model(conversation_history):
#     """Send a query to the Hugging Face API and get a response"""
#     prompt = create_prompt(conversation_history)
    
#     # Prepare the payload
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 300,
#             "temperature": 0.7,
#             "top_p": 0.9,
#             "do_sample": True
#         }
#     }
    
#     # Send the request
#     try:
#         response = requests.post(config.API_URL, headers=headers, json=payload)
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             result = response.json()
#             if isinstance(result, list) and len(result) > 0:
#                 # Only return the actual response, not the whole conversation
#                 generated_text = result[0].get("generated_text", "")
#                 # Remove the prompt from the response
#                 response_text = generated_text.replace(prompt, "")
#                 # Extract only the first response (up to next "User:" if present)
#                 if "User:" in response_text:
#                     response_text = response_text.split("User:")[0].strip()
                
#                 return response_text
#             return str(result)
#         else:
#             print(f"Error: {response.status_code}")
#             print(response.text)
#             return "I'm sorry, I encountered an error while processing your request."
#     except Exception as e:
#         print(f"Exception occurred: {str(e)}")
#         return "I'm sorry, I encountered an error while processing your request."

# def process_user_message(user_id, message, conversation_history=None):
#     """Process a user message and return the response.
    
#     This function is designed to be used in different interfaces (CLI, web, etc.)
#     """
#     # Initialize or get conversation history
#     if conversation_history is None:
#         # Get user history if user_id is provided
#         if user_id:
#             user_data = user_manager.get_user(user_id)
#             if user_data and "conversation_history" in user_data:
#                 conversation_history = user_data.get("conversation_history", [])
#             else:
#                 conversation_history = []
#         else:
#             conversation_history = []
    
#     # Add user message to conversation history
#     conversation_history.append({"role": "user", "content": message})
    
#     # Get response from the model
#     response = query_model(conversation_history)
    
#     # Enrich response with knowledge base information
#     enriched_response = enrich_response_with_knowledge(message, response, user_id)
    
#     # Add assistant response to conversation history
#     conversation_history.append({"role": "assistant", "content": enriched_response})
    
#     # Save conversation if user_id is provided
#     if user_id:
#         conversation = {
#             "user": message,
#             "assistant": enriched_response
#         }
#         user_manager.add_conversation(user_id, conversation)
    
#     return enriched_response, conversation_history

# def cli_interface():
#     """Command-line interface for the chatbot."""
#     print("Welcome to Counselmate - Your AI Career Counselor!")
#     print("Type 'exit' to end the conversation.")
#     print("Type 'new user' to create a user profile.")
#     print("Type 'login' to use an existing profile.\n")
    
#     user_id = None
#     conversation_history = []
    
#     # Add welcome message to conversation history
#     welcome_message = "Hello! I'm Counselmate, your AI career counselor. I'm here to help you explore career options and provide guidance based on your interests, skills, and goals. What would you like to discuss about your career journey today?"
#     conversation_history.append({"role": "assistant", "content": welcome_message})
    
#     # Print the welcome message
#     print("Counselmate:", welcome_message)
    
#     # Main conversation loop
#     while True:
#         # Get user input
#         user_input = input("\nYou: ")
        
#         # Check if user wants to exit
#         if user_input.lower() == 'exit':
#             print("\nCounsellor: Thank you for using Counselmate! Good luck with your career journey!")
#             break
        
#         # Check if user wants to create new profile
#         elif user_input.lower() == 'new user':
#             name = input("Enter your name: ")
#             email = input("Enter your email (optional): ")
#             education = input("Enter your current education level (optional): ")
            
#             # Generate unique user ID
#             new_user_id = str(uuid.uuid4())
            
#             # Create user profile
#             if user_manager.create_user(new_user_id, name, email, education):
#                 user_id = new_user_id
#                 print(f"\nProfile created successfully! Your user ID is: {user_id}")
#                 print("Please save this ID for future logins.")
#             else:
#                 print("\nError creating profile. Please try again.")
            
#             continue
        
#         # Check if user wants to login
#         elif user_input.lower() == 'login':
#             login_id = input("Enter your user ID: ")
#             user_data = user_manager.get_user(login_id)
            
#             if user_data:
#                 user_id = login_id
#                 print(f"\nWelcome back, {user_data['name']}!")
                
#                 # Get conversation history for the user
#                 history = user_manager.get_conversation_history(user_id)
#                 if history:
#                     # Convert to the format expected by process_user_message
#                     conversation_history = []
#                     for convo in history:
#                         conversation_history.append({"role": "user", "content": convo["user"]})
#                         conversation_history.append({"role": "assistant", "content": convo["assistant"]})
#             else:
#                 print("\nUser not found. Please check your ID or create a new profile.")
            
#             continue
        
#         # Process normal chat input
#         response, conversation_history = process_user_message(user_id, user_input, conversation_history)
        
#         # Print response
#         print("\nCounsellor:", response)

# if __name__ == "__main__":

#     # Start the CLI interface
#     cli_interface()

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import json
import uuid
import requests
from career_knowledge_base import CareerKnowledgeBase
from user_profile_manager import UserProfileManager
import config

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

try:
    kb = CareerKnowledgeBase()
    user_manager = UserProfileManager()
except Exception as e:
    print(f"Failed to initialize database connections: {e}")

# Headers for API request
headers = {
    "Authorization": f"Bearer {config.API_TOKEN}",
    "Content-Type": "application/json"
}

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
    prompt = config.SYSTEM_PROMPT + "\n\n"
    
    for message in conversation_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            prompt += f"User: {content}\n"
        else:
            prompt += f"Counselmate: {content}\n"
    
    prompt += "Counselmate: "
    return prompt

def query_model(conversation_history):
    prompt = create_prompt(conversation_history)
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(config.API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                response_text = generated_text.replace(prompt, "")
                if "User:" in response_text:
                    response_text = response_text.split("User:")[0].strip()
                return response_text
            return str(result)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return "I'm sorry, I encountered an error while processing your request."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    conversation_history = data.get('conversation_history', [])
    
    response, updated_history = process_user_message(user_id, message, conversation_history)
    
    return jsonify({
        'response': response,
        'conversation_history': updated_history
    })

@app.route('/api/user/create', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email', None)
    education_level = data.get('education_level', None)
    
    user_id = str(uuid.uuid4())
    
    if user_manager.create_user(user_id, name, email, education_level):
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User created successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to create user'
        }), 400

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user_data = user_manager.get_user(user_id)
    if user_data:
        # Remove MongoDB _id field
        user_data.pop('_id', None)
        return jsonify({
            'success': True,
            'user': user_data
        })
    else:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404

@app.route('/api/careers/suggest', methods=['POST'])
def suggest_careers():
    data = request.get_json()
    interests = data.get('interests', [])
    skills = data.get('skills', [])
    education = data.get('education', None)
    
    careers = []
    
    if interests and skills:
        careers = kb.search_by_skills(skills, top_n=5) + kb.search_by_interests(interests, top_n=5)
    elif interests:
        careers = kb.search_by_interests(interests, top_n=5)
    elif skills:
        careers = kb.search_by_skills(skills, top_n=5)
    elif education:
        careers = kb.search_by_education(education, top_n=5)
    
    # Remove duplicates
    seen = set()
    unique_careers = []
    for career in careers:
        if career['title'] not in seen:
            seen.add(career['title'])
            unique_careers.append(career)
    
    return jsonify({
        'success': True,
        'careers': unique_careers[:5]  # Return top 5
    })

def process_user_message(user_id, message, conversation_history=None):
    if conversation_history is None:
        if user_id:
            user_data = user_manager.get_user(user_id)
            if user_data and "conversation_history" in user_data:
                conversation_history = user_data.get("conversation_history", [])
            else:
                conversation_history = []
        else:
            conversation_history = []
    
    conversation_history.append({"role": "user", "content": message})
    response = query_model(conversation_history)
    enriched_response = enrich_response_with_knowledge(message, response, user_id)
    conversation_history.append({"role": "assistant", "content": enriched_response})
    
    if user_id:
        conversation = {
            "user": message,
            "assistant": enriched_response
        }
        user_manager.add_conversation(user_id, conversation)
    
    return enriched_response, conversation_history

if __name__ == '__main__':
    app.run(debug=True, port=5000)