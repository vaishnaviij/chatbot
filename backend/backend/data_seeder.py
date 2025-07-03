"""
Data seeder for Counselmate - AI Career Counselor Chatbot

This script populates the initial career database in MongoDB with relevant information
about various career paths, including descriptions, required skills, education
paths, and salary ranges in Indian context.
"""

import os
import json
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, CAREER_DATA_COLLECTION

def create_career_data():
    """Create initial career data for the knowledge base with Indian salary ranges."""
    
    careers = [
        {
            "title": "Software Developer",
            "description": "Designs, builds, and maintains computer programs and applications.",
            "required_skills": ["programming", "problem-solving", "analytical thinking", "debugging", "teamwork"],
            "education_paths": ["Computer Science degree", "Coding Bootcamp", "Self-taught with portfolio"],
            "avg_salary_range": {
                "entry": "₹4,00,000 - ₹6,00,000",
                "mid": "₹8,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["technology", "problem-solving", "building", "designing", "analytical"]
        },
        {
            "title": "Data Scientist",
            "description": "Analyzes complex data to help businesses make better decisions.",
            "required_skills": ["statistics", "programming", "data analysis", "machine learning", "communication"],
            "education_paths": ["Statistics degree", "Computer Science degree", "Data Science bootcamp", "Mathematics degree"],
            "avg_salary_range": {
                "entry": "₹5,00,000 - ₹7,00,000",
                "mid": "₹10,00,000 - ₹15,00,000",
                "senior": "₹18,00,000 - ₹30,00,000+"
            },
            "related_interests": ["analysis", "technology", "problem-solving", "research", "analytical"]
        },
        {
            "title": "Registered Nurse",
            "description": "Provides patient care, education, and emotional support in healthcare settings.",
            "required_skills": ["patient care", "communication", "empathy", "critical thinking", "organization"],
            "education_paths": ["Nursing degree", "Nursing diploma", "Associate's degree in Nursing"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,00,000",
                "mid": "₹4,50,000 - ₹7,00,000",
                "senior": "₹8,00,000 - ₹12,00,000+"
            },
            "related_interests": ["healthcare", "helping people", "science", "problem-solving", "working with people"]
        },
        {
            "title": "Digital Marketing Specialist",
            "description": "Develops and implements marketing strategies through digital channels.",
            "required_skills": ["social media", "content creation", "data analysis", "SEO", "communication"],
            "education_paths": ["Marketing degree", "Communications degree", "Digital Marketing certification"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,50,000",
                "mid": "₹5,00,000 - ₹8,00,000",
                "senior": "₹10,00,000 - ₹15,00,000+"
            },
            "related_interests": ["creative", "communication", "writing", "analysis", "business"]
        },
        {
            "title": "School Teacher",
            "description": "Educates students in various subjects and facilitates their development.",
            "required_skills": ["teaching", "patience", "communication", "organization", "creativity"],
            "education_paths": ["Education degree", "Teaching certification", "Subject-specific degree"],
            "avg_salary_range": {
                "entry": "₹2,00,000 - ₹3,50,000",
                "mid": "₹4,00,000 - ₹6,00,000",
                "senior": "₹7,00,000 - ₹10,00,000+"
            },
            "related_interests": ["teaching", "helping people", "working with children", "creative", "communication"]
        },
        {
            "title": "Graphic Designer",
            "description": "Creates visual concepts to communicate ideas that inspire, inform, or captivate consumers.",
            "required_skills": ["design software", "creativity", "typography", "visual communication", "problem-solving"],
            "education_paths": ["Graphic Design degree", "Fine Arts degree", "Design bootcamp", "Self-taught with portfolio"],
            "avg_salary_range": {
                "entry": "₹2,00,000 - ₹3,50,000",
                "mid": "₹4,00,000 - ₹6,00,000",
                "senior": "₹7,00,000 - ₹12,00,000+"
            },
            "related_interests": ["art", "creative", "designing", "visual arts", "communication"]
        },
        {
            "title": "Financial Analyst",
            "description": "Evaluates investment opportunities and provides financial guidance to businesses and individuals.",
            "required_skills": ["financial modeling", "data analysis", "research", "attention to detail", "communication"],
            "education_paths": ["Finance degree", "Accounting degree", "Economics degree", "MBA"],
            "avg_salary_range": {
                "entry": "₹3,50,000 - ₹5,50,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["business", "analytical", "problem-solving", "math", "research"]
        },
        {
            "title": "Doctor (MBBS)",
            "description": "Diagnoses and treats patients' medical conditions in various healthcare settings.",
            "required_skills": ["medical knowledge", "diagnosis", "communication", "empathy", "decision making"],
            "education_paths": ["MBBS degree", "Medical entrance exam preparation"],
            "avg_salary_range": {
                "entry": "₹6,00,000 - ₹10,00,000",
                "mid": "₹12,00,000 - ₹20,00,000",
                "senior": "₹25,00,000 - ₹50,00,000+"
            },
            "related_interests": ["healthcare", "helping people", "science", "biology", "problem-solving"]
        },
        {
            "title": "Human Resources Manager",
            "description": "Oversees recruitment, employee relations, benefits, and training within organizations.",
            "required_skills": ["interpersonal communication", "conflict resolution", "organization", "leadership", "decision making"],
            "education_paths": ["Human Resources degree", "Business Administration degree", "Psychology degree"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹9,00,000",
                "senior": "₹12,00,000 - ₹18,00,000+"
            },
            "related_interests": ["working with people", "business", "communication", "problem-solving", "organization"]
        },
        {
            "title": "Civil Engineer",
            "description": "Designs, builds, and maintains infrastructure projects like roads, buildings, and bridges.",
            "required_skills": ["mathematics", "physics", "CAD software", "problem-solving", "project management"],
            "education_paths": ["Civil Engineering degree", "Engineering Technology degree"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["building", "designing", "problem-solving", "analytical", "math"]
        },
        {
            "title": "Chartered Accountant (CA)",
            "description": "Provides financial advice, audits accounts, and provides trustworthy information about financial records.",
            "required_skills": ["accounting", "taxation", "auditing", "financial reporting", "attention to detail"],
            "education_paths": ["CA certification", "Commerce degree with CA articleship"],
            "avg_salary_range": {
                "entry": "₹6,00,000 - ₹9,00,000",
                "mid": "₹12,00,000 - ₹18,00,000",
                "senior": "₹20,00,000 - ₹40,00,000+"
            },
            "related_interests": ["business", "numbers", "analysis", "problem-solving", "finance"]
        },
        {
            "title": "Pharmacist",
            "description": "Dispenses prescription medications and provides expertise on their proper use.",
            "required_skills": ["pharmaceutical knowledge", "attention to detail", "communication", "customer service", "ethics"],
            "education_paths": ["Pharmacy degree (B.Pharm/D.Pharm)", "Pharmacy entrance exams"],
            "avg_salary_range": {
                "entry": "₹2,00,000 - ₹4,00,000",
                "mid": "₹4,50,000 - ₹7,00,000",
                "senior": "₹8,00,000 - ₹12,00,000+"
            },
            "related_interests": ["healthcare", "science", "medicine", "helping people", "chemistry"]
        },
        {
            "title": "Journalist",
            "description": "Researches and reports news stories for newspapers, magazines, television, or online platforms.",
            "required_skills": ["writing", "research", "interviewing", "communication", "critical thinking"],
            "education_paths": ["Journalism degree", "Mass Communication degree", "English Literature degree"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,50,000",
                "mid": "₹5,00,000 - ₹8,00,000",
                "senior": "₹10,00,000 - ₹15,00,000+"
            },
            "related_interests": ["writing", "current affairs", "communication", "research", "storytelling"]
        },
        {
            "title": "Hotel Manager",
            "description": "Oversees operations in hotels, resorts, or other hospitality establishments.",
            "required_skills": ["customer service", "management", "organization", "communication", "problem-solving"],
            "education_paths": ["Hotel Management degree", "Hospitality Management degree", "Business Administration degree"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["hospitality", "management", "working with people", "organization", "customer service"]
        },
        {
            "title": "Architect",
            "description": "Designs buildings and oversees their construction, ensuring functionality and aesthetics.",
            "required_skills": ["design", "creativity", "CAD software", "spatial reasoning", "project management"],
            "education_paths": ["Architecture degree", "Design degree with architecture specialization"],
            "avg_salary_range": {
                "entry": "₹4,00,000 - ₹6,00,000",
                "mid": "₹8,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["designing", "creative", "building", "art", "problem-solving"]
        },
        {
            "title": "Fashion Designer",
            "description": "Creates clothing, accessories, and footwear designs for various markets.",
            "required_skills": ["creativity", "design", "sewing", "trend analysis", "visualization"],
            "education_paths": ["Fashion Design degree", "Textile Design degree", "Design diploma"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,50,000",
                "mid": "₹5,00,000 - ₹8,00,000",
                "senior": "₹10,00,000 - ₹20,00,000+"
            },
            "related_interests": ["fashion", "creative", "designing", "art", "trends"]
        },
        {
            "title": "Police Officer",
            "description": "Maintains law and order, prevents crime, and protects citizens.",
            "required_skills": ["physical fitness", "communication", "problem-solving", "ethics", "quick decision making"],
            "education_paths": ["Police academy training", "Criminal Justice degree", "Physical fitness training"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹9,00,000",
                "senior": "₹10,00,000 - ₹15,00,000+"
            },
            "related_interests": ["public service", "law enforcement", "helping people", "problem-solving", "physical activity"]
        },
        {
            "title": "Mechanical Engineer",
            "description": "Designs, develops, and tests mechanical devices and systems.",
            "required_skills": ["mechanical design", "problem-solving", "CAD software", "physics", "mathematics"],
            "education_paths": ["Mechanical Engineering degree", "Engineering diploma"],
            "avg_salary_range": {
                "entry": "₹3,50,000 - ₹5,50,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["mechanics", "designing", "problem-solving", "building", "analytical"]
        },
        {
            "title": "Psychologist",
            "description": "Studies mental processes and behavior, and provides therapy to individuals.",
            "required_skills": ["listening", "empathy", "analysis", "communication", "research"],
            "education_paths": ["Psychology degree", "Clinical Psychology degree", "Counseling certification"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹18,00,000+"
            },
            "related_interests": ["helping people", "mental health", "research", "communication", "problem-solving"]
        },
        {
            "title": "Airline Pilot",
            "description": "Operates aircraft to transport passengers and cargo on scheduled flights.",
            "required_skills": ["aviation knowledge", "quick decision making", "attention to detail", "stress management", "teamwork"],
            "education_paths": ["Commercial Pilot License", "Aviation degree", "Flight school training"],
            "avg_salary_range": {
                "entry": "₹8,00,000 - ₹12,00,000",
                "mid": "₹15,00,000 - ₹25,00,000",
                "senior": "₹30,00,000 - ₹50,00,000+"
            },
            "related_interests": ["aviation", "travel", "technology", "adventure", "mechanics"]
        },
        {
            "title": "Cybersecurity Analyst",
            "description": "Protects computer systems and networks from cyber threats and security breaches.",
            "required_skills": ["network security", "ethical hacking", "risk assessment", "problem-solving", "attention to detail"],
            "education_paths": ["Computer Science degree with cybersecurity specialization", "Cybersecurity certifications (CEH, CISSP)", "Information Technology degree"],
            "avg_salary_range": {
                "entry": "₹5,00,000 - ₹7,00,000",
                "mid": "₹10,00,000 - ₹15,00,000",
                "senior": "₹18,00,000 - ₹30,00,000+"
            },
            "related_interests": ["technology", "security", "problem-solving", "analytical", "research"]
        },
        {
            "title": "Artificial Intelligence Engineer",
            "description": "Develops AI models and systems to automate tasks and improve decision-making.",
            "required_skills": ["machine learning", "Python programming", "data modeling", "algorithm design", "statistics"],
            "education_paths": ["Computer Science degree with AI specialization", "Data Science degree", "AI/ML certification courses"],
            "avg_salary_range": {
                "entry": "₹6,00,000 - ₹9,00,000",
                "mid": "₹12,00,000 - ₹20,00,000",
                "senior": "₹25,00,000 - ₹40,00,000+"
            },
            "related_interests": ["technology", "innovation", "problem-solving", "research", "analytical"]
        },
        {
            "title": "Blockchain Developer",
            "description": "Designs and implements blockchain-based applications and smart contracts.",
            "required_skills": ["blockchain protocols", "smart contracts", "cryptography", "problem-solving", "distributed systems"],
            "education_paths": ["Computer Science degree", "Blockchain specialization courses", "Cryptography background"],
            "avg_salary_range": {
                "entry": "₹7,00,000 - ₹10,00,000",
                "mid": "₹15,00,000 - ₹25,00,000",
                "senior": "₹30,00,000 - ₹50,00,000+"
            },
            "related_interests": ["technology", "finance", "innovation", "problem-solving", "mathematics"]
        },
        {
            "title": "Robotics Engineer",
            "description": "Designs, builds, and maintains robots and robotic systems.",
            "required_skills": ["mechanical engineering", "programming", "electronics", "control systems", "problem-solving"],
            "education_paths": ["Robotics Engineering degree", "Mechanical Engineering with robotics specialization", "Electronics Engineering"],
            "avg_salary_range": {
                "entry": "₹5,00,000 - ₹8,00,000",
                "mid": "₹10,00,000 - ₹18,00,000",
                "senior": "₹20,00,000 - ₹35,00,000+"
            },
            "related_interests": ["technology", "engineering", "innovation", "problem-solving", "mechanics"]
        },
        {
            "title": "Biomedical Engineer",
            "description": "Develops medical equipment and devices to improve healthcare.",
            "required_skills": ["biology knowledge", "engineering principles", "problem-solving", "medical device regulations", "research"],
            "education_paths": ["Biomedical Engineering degree", "Biotechnology degree", "Medical equipment specialization"],
            "avg_salary_range": {
                "entry": "₹4,00,000 - ₹6,00,000",
                "mid": "₹8,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["healthcare", "technology", "innovation", "problem-solving", "biology"]
        },
        {
            "title": "Renewable Energy Engineer",
            "description": "Designs and implements sustainable energy solutions like solar and wind power systems.",
            "required_skills": ["energy systems", "sustainability", "project management", "problem-solving", "environmental regulations"],
            "education_paths": ["Renewable Energy Engineering degree", "Electrical Engineering with energy specialization", "Environmental Engineering"],
            "avg_salary_range": {
                "entry": "₹4,50,000 - ₹7,00,000",
                "mid": "₹9,00,000 - ₹15,00,000",
                "senior": "₹18,00,000 - ₹30,00,000+"
            },
            "related_interests": ["environment", "technology", "sustainability", "problem-solving", "innovation"]
        },
        {
            "title": "UI/UX Designer",
            "description": "Creates user-friendly interfaces and enhances user experience for digital products.",
            "required_skills": ["design thinking", "prototyping", "user research", "creativity", "communication"],
            "education_paths": ["Design degree", "Human-Computer Interaction degree", "UI/UX certification courses"],
            "avg_salary_range": {
                "entry": "₹4,00,000 - ₹6,00,000",
                "mid": "₹8,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["design", "technology", "psychology", "problem-solving", "creative"]
        },
        {
            "title": "Cloud Architect",
            "description": "Designs and manages cloud computing strategies and infrastructure for organizations.",
            "required_skills": ["cloud platforms (AWS/Azure/GCP)", "networking", "security", "system design", "problem-solving"],
            "education_paths": ["Computer Science degree", "Cloud certifications (AWS, Azure)", "Information Technology degree"],
            "avg_salary_range": {
                "entry": "₹6,00,000 - ₹9,00,000",
                "mid": "₹12,00,000 - ₹20,00,000",
                "senior": "₹25,00,000 - ₹40,00,000+"
            },
            "related_interests": ["technology", "infrastructure", "problem-solving", "analytical", "networking"]
        },
        {
            "title": "Data Engineer",
            "description": "Builds and maintains systems for collecting, storing, and processing large datasets.",
            "required_skills": ["database management", "ETL processes", "big data technologies", "programming", "problem-solving"],
            "education_paths": ["Computer Science degree", "Data Engineering specialization", "Information Technology degree"],
            "avg_salary_range": {
                "entry": "₹5,00,000 - ₹8,00,000",
                "mid": "₹10,00,000 - ₹16,00,000",
                "senior": "₹20,00,000 - ₹35,00,000+"
            },
            "related_interests": ["technology", "data", "problem-solving", "analytical", "systems"]
        },
        {
            "title": "Game Developer",
            "description": "Creates video games for various platforms including mobile, console, and PC.",
            "required_skills": ["game engines (Unity/Unreal)", "programming", "3D modeling", "creativity", "problem-solving"],
            "education_paths": ["Game Development degree", "Computer Science degree with game specialization", "Animation degree"],
            "avg_salary_range": {
                "entry": "₹3,50,000 - ₹6,00,000",
                "mid": "₹7,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["gaming", "technology", "creative", "problem-solving", "design"]
        },
        {
            "title": "Ethical Hacker",
            "description": "Identifies vulnerabilities in computer systems to improve security.",
            "required_skills": ["penetration testing", "network security", "programming", "problem-solving", "attention to detail"],
            "education_paths": ["Computer Science degree", "Cybersecurity certifications (CEH, OSCP)", "Information Technology degree"],
            "avg_salary_range": {
                "entry": "₹6,00,000 - ₹9,00,000",
                "mid": "₹12,00,000 - ₹20,00,000",
                "senior": "₹25,00,000 - ₹40,00,000+"
            },
            "related_interests": ["technology", "security", "problem-solving", "analytical", "research"]
        },
        {
            "title": "IoT Solutions Architect",
            "description": "Designs and implements Internet of Things systems and solutions.",
            "required_skills": ["embedded systems", "networking", "cloud computing", "data analytics", "problem-solving"],
            "education_paths": ["Computer Science degree", "Electronics Engineering", "IoT specialization courses"],
            "avg_salary_range": {
                "entry": "₹5,00,000 - ₹8,00,000",
                "mid": "₹10,00,000 - ₹18,00,000",
                "senior": "₹20,00,000 - ₹35,00,000+"
            },
            "related_interests": ["technology", "innovation", "problem-solving", "analytical", "systems"]
        },
        {
            "title": "Quantum Computing Scientist",
            "description": "Researches and develops quantum computing algorithms and systems.",
            "required_skills": ["quantum mechanics", "linear algebra", "programming", "research", "problem-solving"],
            "education_paths": ["Physics degree with quantum specialization", "Computer Science degree with quantum focus", "Mathematics degree"],
            "avg_salary_range": {
                "entry": "₹8,00,000 - ₹12,00,000",
                "mid": "₹15,00,000 - ₹25,00,000",
                "senior": "₹30,00,000 - ₹50,00,000+"
            },
            "related_interests": ["technology", "physics", "research", "problem-solving", "mathematics"]
        },
        {
            "title": "AR/VR Developer",
            "description": "Creates augmented and virtual reality experiences and applications.",
            "required_skills": ["3D modeling", "game engines (Unity/Unreal)", "programming", "creativity", "problem-solving"],
            "education_paths": ["Computer Science degree", "Game Development degree", "AR/VR specialization courses"],
            "avg_salary_range": {
                "entry": "₹5,00,000 - ₹8,00,000",
                "mid": "₹10,00,000 - ₹16,00,000",
                "senior": "₹20,00,000 - ₹35,00,000+"
            },
            "related_interests": ["technology", "gaming", "creative", "problem-solving", "design"]
        },
        {
            "title": "DevOps Engineer",
            "description": "Bridges development and operations to improve software delivery and infrastructure.",
            "required_skills": ["CI/CD pipelines", "cloud platforms", "automation", "scripting", "problem-solving"],
            "education_paths": ["Computer Science degree", "Information Technology degree", "DevOps certification courses"],
            "avg_salary_range": {
                "entry": "₹6,00,000 - ₹9,00,000",
                "mid": "₹12,00,000 - ₹20,00,000",
                "senior": "₹25,00,000 - ₹40,00,000+"
            },
            "related_interests": ["technology", "systems", "problem-solving", "automation", "infrastructure"]
        },
            {
        "title": "Digital Content Creator",
        "description": "Creates engaging content for digital platforms like YouTube, Instagram, and blogs.",
        "required_skills": ["content creation", "video editing", "social media", "creativity", "storytelling"],
        "education_paths": ["Mass Communication degree", "Digital Marketing courses", "Self-taught with portfolio"],
        "avg_salary_range": {
            "entry": "₹2,50,000 - ₹4,50,000",
            "mid": "₹6,00,000 - ₹10,00,000",
            "senior": "₹12,00,000 - ₹20,00,000+"
        },
        "related_interests": ["creative", "social media", "writing", "entertainment", "communication"]
        },
        {
            "title": "Nutritionist/Dietician",
            "description": "Provides dietary advice and nutrition plans to improve health and wellness.",
            "required_skills": ["nutrition knowledge", "communication", "meal planning", "health assessment", "empathy"],
            "education_paths": ["Nutrition and Dietetics degree", "Food Science degree", "Clinical Nutrition courses"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹9,00,000",
                "senior": "₹12,00,000 - ₹18,00,000+"
            },
            "related_interests": ["health", "food", "science", "helping people", "wellness"]
        },
        {
            "title": "Event Manager",
            "description": "Plans and executes events like weddings, corporate meetings, and concerts.",
            "required_skills": ["organization", "budgeting", "vendor management", "creativity", "problem-solving"],
            "education_paths": ["Event Management degree", "Hospitality Management degree", "Business Administration degree"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["planning", "creative", "management", "working with people", "organization"]
        },
        {
            "title": "Interior Designer",
            "description": "Designs functional and aesthetically pleasing interior spaces for homes and businesses.",
            "required_skills": ["space planning", "color theory", "CAD software", "creativity", "client communication"],
            "education_paths": ["Interior Design degree", "Architecture degree", "Design diploma"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["design", "creative", "architecture", "art", "space planning"]
        },
        {
            "title": "Travel Consultant",
            "description": "Plans and books travel arrangements for individuals and groups.",
            "required_skills": ["destination knowledge", "customer service", "booking systems", "communication", "problem-solving"],
            "education_paths": ["Travel & Tourism degree", "Hospitality Management degree", "Tourism certification"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,00,000",
                "mid": "₹5,00,000 - ₹8,00,000",
                "senior": "₹10,00,000 - ₹15,00,000+"
            },
            "related_interests": ["travel", "geography", "customer service", "planning", "culture"]
        },
        {
            "title": "Fitness Trainer",
            "description": "Helps clients achieve fitness goals through exercise programs and nutrition advice.",
            "required_skills": ["exercise science", "motivation", "communication", "anatomy knowledge", "demonstration"],
            "education_paths": ["Sports Science degree", "Fitness certification courses", "Physical Education degree"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,50,000",
                "mid": "₹5,00,000 - ₹8,00,000",
                "senior": "₹10,00,000 - ₹15,00,000+"
            },
            "related_interests": ["fitness", "health", "sports", "helping people", "physical activity"]
        },
        {
            "title": "Career Counselor",
            "description": "Guides individuals in making educational and career decisions.",
            "required_skills": ["active listening", "assessment tools", "communication", "empathy", "career knowledge"],
            "education_paths": ["Psychology degree", "Career Counseling certification", "Human Resources degree"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹9,00,000",
                "senior": "₹12,00,000 - ₹18,00,000+"
            },
            "related_interests": ["helping people", "psychology", "education", "communication", "mentoring"]
        },
        {
            "title": "Foreign Language Translator",
            "description": "Converts written materials from one language to another while preserving meaning.",
            "required_skills": ["language proficiency", "writing", "cultural knowledge", "attention to detail", "research"],
            "education_paths": ["Language degree", "Translation certification", "Study abroad experience"],
            "avg_salary_range": {
                "entry": "₹3,50,000 - ₹6,00,000",
                "mid": "₹7,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["languages", "writing", "culture", "communication", "literature"]
        },
        {
            "title": "Forensic Scientist",
            "description": "Analyzes physical evidence from crime scenes to help solve criminal cases.",
            "required_skills": ["scientific analysis", "attention to detail", "report writing", "problem-solving", "chemistry knowledge"],
            "education_paths": ["Forensic Science degree", "Chemistry degree", "Biology degree"],
            "avg_salary_range": {
                "entry": "₹4,00,000 - ₹6,00,000",
                "mid": "₹8,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["science", "investigation", "problem-solving", "analytical", "research"]
        },
        {
            "title": "Animation Artist",
            "description": "Creates animated visuals for films, games, and advertisements using digital tools.",
            "required_skills": ["animation software", "drawing", "storyboarding", "creativity", "attention to detail"],
            "education_paths": ["Animation degree", "Fine Arts degree", "Animation diploma courses"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["art", "creative", "storytelling", "technology", "visual arts"]
        },
        {
            "title": "Radio Jockey",
            "description": "Hosts radio programs, engages with listeners, and plays music.",
            "required_skills": ["voice modulation", "communication", "scripting", "quick thinking", "entertainment"],
            "education_paths": ["Mass Communication degree", "Journalism degree", "Radio Production courses"],
            "avg_salary_range": {
                "entry": "₹2,50,000 - ₹4,50,000",
                "mid": "₹5,00,000 - ₹8,00,000",
                "senior": "₹10,00,000 - ₹15,00,000+"
            },
            "related_interests": ["entertainment", "communication", "music", "current affairs", "public speaking"]
        },
        {
            "title": "Wildlife Photographer",
            "description": "Captures images of animals and nature for publications, documentaries, and art.",
            "required_skills": ["photography", "patience", "wildlife knowledge", "editing", "adventure"],
            "education_paths": ["Photography degree", "Wildlife Biology degree", "Self-taught with portfolio"],
            "avg_salary_range": {
                "entry": "₹2,00,000 - ₹4,00,000",
                "mid": "₹5,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["photography", "nature", "animals", "art", "adventure"]
        },
        {
            "title": "Museum Curator",
            "description": "Manages collections of artifacts or works of art and organizes exhibitions.",
            "required_skills": ["art/history knowledge", "research", "organization", "communication", "preservation"],
            "education_paths": ["Art History degree", "Museum Studies degree", "Archaeology degree"],
            "avg_salary_range": {
                "entry": "₹3,50,000 - ₹5,50,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹18,00,000+"
            },
            "related_interests": ["history", "art", "research", "culture", "education"]
        },
        {
            "title": "Podcast Producer",
            "description": "Creates and manages podcast content from concept to publication.",
            "required_skills": ["audio editing", "storytelling", "research", "communication", "content planning"],
            "education_paths": ["Media Studies degree", "Journalism degree", "Audio Production courses"],
            "avg_salary_range": {
                "entry": "₹3,00,000 - ₹5,00,000",
                "mid": "₹6,00,000 - ₹10,00,000",
                "senior": "₹12,00,000 - ₹20,00,000+"
            },
            "related_interests": ["media", "storytelling", "communication", "current affairs", "entertainment"]
        },
        {
            "title": "Culinary Arts Instructor",
            "description": "Teaches cooking techniques and culinary arts to students in academic or recreational settings.",
            "required_skills": ["culinary expertise", "teaching", "recipe development", "communication", "demonstration"],
            "education_paths": ["Culinary Arts degree", "Hospitality degree", "Professional chef experience"],
            "avg_salary_range": {
                "entry": "₹3,50,000 - ₹6,00,000",
                "mid": "₹7,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["cooking", "teaching", "food", "creative", "helping people"]
        },
        {
            "title": "Sustainability Consultant",
            "description": "Advises organizations on implementing environmentally sustainable practices.",
            "required_skills": ["environmental knowledge", "data analysis", "communication", "problem-solving", "project management"],
            "education_paths": ["Environmental Science degree", "Sustainability Management degree", "Business with sustainability focus"],
            "avg_salary_range": {
                "entry": "₹4,00,000 - ₹6,00,000",
                "mid": "₹8,00,000 - ₹12,00,000",
                "senior": "₹15,00,000 - ₹25,00,000+"
            },
            "related_interests": ["environment", "business", "problem-solving", "research", "analytical"]
        }

    ]
    
    return careers

def seed_database():
    """Seed the career knowledge database in MongoDB."""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[CAREER_DATA_COLLECTION]
        
        # Check if collection already has data
        if collection.count_documents({}) > 0:
            print("Career data already exists in the database.")
            
            # Ask user if they want to overwrite
            response = input("Do you want to overwrite existing data? (y/n): ")
            if response.lower() != 'y':
                print("Database seeding cancelled.")
                client.close()
                return
        
        # Generate career data
        careers = create_career_data()
        
        # Insert data into MongoDB
        result = collection.insert_many(careers)
        
        print(f"Successfully seeded career database with {len(result.inserted_ids)} careers.")
        print(f"Data saved to MongoDB collection: {DATABASE_NAME}.{CAREER_DATA_COLLECTION}")
        
        client.close()
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")

def add_custom_career():
    """Add a custom career to the existing MongoDB database."""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[CAREER_DATA_COLLECTION]
        
        # Get career information from user
        title = input("Enter career title: ")
        description = input("Enter career description: ")
        
        skills = []
        print("Enter required skills (empty line to finish):")
        while True:
            skill = input("Skill: ")
            if not skill:
                break
            skills.append(skill)
        
        education = []
        print("Enter education paths (empty line to finish):")
        while True:
            path = input("Education path: ")
            if not path:
                break
            education.append(path)
        
        entry_salary = input("Enter entry-level salary range (e.g. ₹4,00,000 - ₹6,00,000): ")
        mid_salary = input("Enter mid-level salary range (e.g. ₹8,00,000 - ₹12,00,000): ")
        senior_salary = input("Enter senior-level salary range (e.g. ₹15,00,000 - ₹25,00,000+): ")
        
        interests = []
        print("Enter related interests (empty line to finish):")
        while True:
            interest = input("Interest: ")
            if not interest:
                break
            interests.append(interest)
        
        # Create new career entry
        new_career = {
            "title": title,
            "description": description,
            "required_skills": skills,
            "education_paths": education,
            "avg_salary_range": {
                "entry": entry_salary,
                "mid": mid_salary,
                "senior": senior_salary
            },
            "related_interests": interests
        }
        
        # Add to careers collection
        result = collection.insert_one(new_career)
        
        print(f"Successfully added {title} to the career database with ID: {result.inserted_id}")
        
        client.close()
        
    except Exception as e:
        print(f"Error adding custom career: {str(e)}")

if __name__ == "__main__":
    print("Counselmate Career Database Seeder")
    print("==================================")
    print("1. Seed database with initial career data")
    print("2. Add a custom career to existing database")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        seed_database()
    elif choice == "2":
        add_custom_career()
    else:
        print("Exiting seeder.")