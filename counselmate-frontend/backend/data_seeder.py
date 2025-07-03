"""
Data seeder for Counselmate - AI Career Counselor Chatbot

This script populates the initial career database with relevant information
about various career paths, including descriptions, required skills, education
paths, and salary ranges.
"""

import os
import json
import backend.config as config

def create_career_data():
    """Create initial career data for the knowledge base."""
    
    careers = [
        {
            "title": "Software Developer",
            "description": "Designs, builds, and maintains computer programs and applications.",
            "required_skills": ["programming", "problem-solving", "analytical thinking", "debugging", "teamwork"],
            "education_paths": ["Computer Science degree", "Coding Bootcamp", "Self-taught with portfolio"],
            "avg_salary_range": {
                "entry": "$60,000",
                "mid": "$85,000",
                "senior": "$120,000+"
            },
            "related_interests": ["technology", "problem-solving", "building", "designing", "analytical"]
        },
        {
            "title": "Data Scientist",
            "description": "Analyzes complex data to help businesses make better decisions.",
            "required_skills": ["statistics", "programming", "data analysis", "machine learning", "communication"],
            "education_paths": ["Statistics degree", "Computer Science degree", "Data Science bootcamp", "Mathematics degree"],
            "avg_salary_range": {
                "entry": "$70,000",
                "mid": "$95,000",
                "senior": "$130,000+"
            },
            "related_interests": ["analysis", "technology", "problem-solving", "research", "analytical"]
        },
        {
            "title": "Registered Nurse",
            "description": "Provides patient care, education, and emotional support in healthcare settings.",
            "required_skills": ["patient care", "communication", "empathy", "critical thinking", "organization"],
            "education_paths": ["Nursing degree", "Nursing diploma", "Associate's degree in Nursing"],
            "avg_salary_range": {
                "entry": "$55,000",
                "mid": "$75,000",
                "senior": "$100,000+"
            },
            "related_interests": ["healthcare", "helping people", "science", "problem-solving", "working with people"]
        },
        {
            "title": "Digital Marketing Specialist",
            "description": "Develops and implements marketing strategies through digital channels.",
            "required_skills": ["social media", "content creation", "data analysis", "SEO", "communication"],
            "education_paths": ["Marketing degree", "Communications degree", "Digital Marketing certification"],
            "avg_salary_range": {
                "entry": "$45,000",
                "mid": "$65,000",
                "senior": "$90,000+"
            },
            "related_interests": ["creative", "communication", "writing", "analysis", "business"]
        },
        {
            "title": "Elementary School Teacher",
            "description": "Educates young students in basic subjects and facilitates their development.",
            "required_skills": ["teaching", "patience", "communication", "organization", "creativity"],
            "education_paths": ["Education degree", "Teaching certification", "Child Development degree"],
            "avg_salary_range": {
                "entry": "$40,000",
                "mid": "$55,000",
                "senior": "$75,000+"
            },
            "related_interests": ["teaching", "helping people", "working with children", "creative", "communication"]
        },
        {
            "title": "Graphic Designer",
            "description": "Creates visual concepts to communicate ideas that inspire, inform, or captivate consumers.",
            "required_skills": ["design software", "creativity", "typography", "visual communication", "problem-solving"],
            "education_paths": ["Graphic Design degree", "Fine Arts degree", "Design bootcamp", "Self-taught with portfolio"],
            "avg_salary_range": {
                "entry": "$40,000",
                "mid": "$60,000",
                "senior": "$85,000+"
            },
            "related_interests": ["art", "creative", "designing", "visual arts", "communication"]
        },
        {
            "title": "Financial Analyst",
            "description": "Evaluates investment opportunities and provides financial guidance to businesses and individuals.",
            "required_skills": ["financial modeling", "data analysis", "research", "attention to detail", "communication"],
            "education_paths": ["Finance degree", "Accounting degree", "Economics degree", "MBA"],
            "avg_salary_range": {
                "entry": "$55,000",
                "mid": "$75,000",
                "senior": "$110,000+"
            },
            "related_interests": ["business", "analytical", "problem-solving", "math", "research"]
        },
        {
            "title": "Veterinarian",
            "description": "Diagnoses and treats animals' medical conditions in various settings.",
            "required_skills": ["animal care", "surgery", "diagnosis", "communication", "empathy"],
            "education_paths": ["Doctor of Veterinary Medicine (DVM)", "Pre-veterinary undergraduate studies"],
            "avg_salary_range": {
                "entry": "$70,000",
                "mid": "$90,000",
                "senior": "$120,000+"
            },
            "related_interests": ["working with animals", "science", "healthcare", "helping", "biology"]
        },
        {
            "title": "Human Resources Manager",
            "description": "Oversees recruitment, employee relations, benefits, and training within organizations.",
            "required_skills": ["interpersonal communication", "conflict resolution", "organization", "leadership", "decision making"],
            "education_paths": ["Human Resources degree", "Business Administration degree", "Psychology degree"],
            "avg_salary_range": {
                "entry": "$55,000",
                "mid": "$75,000",
                "senior": "$110,000+"
            },
            "related_interests": ["working with people", "business", "communication", "problem-solving", "organization"]
        },
        {
            "title": "Environmental Scientist",
            "description": "Studies environmental problems and develops solutions to protect nature and human health.",
            "required_skills": ["research", "data analysis", "field work", "report writing", "problem-solving"],
            "education_paths": ["Environmental Science degree", "Biology degree", "Earth Sciences degree"],
            "avg_salary_range": {
                "entry": "$45,000",
                "mid": "$65,000",
                "senior": "$90,000+"
            },
            "related_interests": ["science", "environment", "research", "analytical", "problem-solving"]
        },
        {
            "title": "Chef",
            "description": "Creates dishes and oversees food preparation in restaurants and other settings.",
            "required_skills": ["cooking techniques", "menu planning", "food safety", "creativity", "time management"],
            "education_paths": ["Culinary Arts degree", "Culinary apprenticeship", "Self-taught with experience"],
            "avg_salary_range": {
                "entry": "$35,000",
                "mid": "$55,000",
                "senior": "$80,000+"
            },
            "related_interests": ["creative", "food", "hands-on work", "art", "designing"]
        },
        {
            "title": "Civil Engineer",
            "description": "Designs, builds, and maintains infrastructure projects like roads, buildings, and bridges.",
            "required_skills": ["mathematics", "physics", "CAD software", "problem-solving", "project management"],
            "education_paths": ["Civil Engineering degree", "Engineering Technology degree"],
            "avg_salary_range": {
                "entry": "$60,000",
                "mid": "$80,000",
                "senior": "$110,000+"
            },
            "related_interests": ["building", "designing", "problem-solving", "analytical", "math"]
        },
        {
            "title": "Physical Therapist",
            "description": "Helps patients improve movement and manage pain after injuries or illnesses.",
            "required_skills": ["anatomy knowledge", "patient care", "communication", "physical stamina", "problem-solving"],
            "education_paths": ["Doctor of Physical Therapy (DPT)", "Physical Therapy undergraduate prerequisites"],
            "avg_salary_range": {
                "entry": "$70,000",
                "mid": "$85,000",
                "senior": "$100,000+"
            },
            "related_interests": ["healthcare", "helping people", "science", "working with people", "physical activity"]
        },
        {
            "title": "Social Worker",
            "description": "Helps people cope with challenges and advocates for vulnerable populations.",
            "required_skills": ["empathy", "communication", "problem-solving", "cultural competence", "organization"],
            "education_paths": ["Social Work degree (BSW/MSW)", "Psychology degree", "Sociology degree"],
            "avg_salary_range": {
                "entry": "$40,000",
                "mid": "$55,000",
                "senior": "$75,000+"
            },
            "related_interests": ["helping people", "communication", "problem-solving", "working with people", "advocacy"]
        },
        {
            "title": "UX Designer",
            "description": "Creates intuitive and enjoyable digital experiences for users.",
            "required_skills": ["user research", "wireframing", "prototyping", "design software", "empathy"],
            "education_paths": ["Design degree", "Human Computer Interaction degree", "UX certification", "Self-taught with portfolio"],
            "avg_salary_range": {
                "entry": "$60,000",
                "mid": "$85,000",
                "senior": "$115,000+"
            },
            "related_interests": ["designing", "creative", "technology", "problem-solving", "research"]
        }
    ]
    
    return careers

def seed_database():
    """Seed the career knowledge database."""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(config.CAREER_DATA_FILE), exist_ok=True)
    
    # Check if the file already exists
    if os.path.exists(config.CAREER_DATA_FILE):
        print(f"Career data file already exists at {config.CAREER_DATA_FILE}")
        
        # Ask user if they want to overwrite
        response = input("Do you want to overwrite existing data? (y/n): ")
        if response.lower() != 'y':
            print("Database seeding cancelled.")
            return
    
    # Generate career data
    careers = create_career_data()
    
    # Save to file
    with open(config.CAREER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(careers, f, indent=2)
    
    print(f"Successfully seeded career database with {len(careers)} careers.")
    print(f"Data saved to {config.CAREER_DATA_FILE}")

def add_custom_career():
    """Add a custom career to the existing database."""
    # Check if the file exists
    if not os.path.exists(config.CAREER_DATA_FILE):
        print("Career database not found. Please run seed_database() first.")
        return
    
    # Load existing data
    with open(config.CAREER_DATA_FILE, 'r', encoding='utf-8') as f:
        careers = json.load(f)
    
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
    
    entry_salary = input("Enter entry-level salary range (e.g. $40,000): ")
    mid_salary = input("Enter mid-level salary range (e.g. $60,000): ")
    senior_salary = input("Enter senior-level salary range (e.g. $80,000+): ")
    
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
    
    # Add to careers list
    careers.append(new_career)
    
    # Save to file
    with open(config.CAREER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(careers, f, indent=2)
    
    print(f"Successfully added {title} to the career database.")

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