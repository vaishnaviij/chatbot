CounselMate – AI-Powered Career Counseling System

CounselMate is an intelligent, interactive career guidance system designed to help students, graduates, and professionals make well-informed decisions about their future career paths. Using a combination of Natural Language Processing (NLP), a curated career knowledge base, and an intuitive chat-based interface, CounselMate simulates the role of a professional career counselor — available 24/7.

Through a personalized conversation, users can share their interests, skills, academic backgrounds, and aspirations. The AI model then analyzes the input, extracts relevant information, and matches it against a structured database of real-world careers to provide tailored recommendations. Whether you're passionate about science, design, teaching, writing, or public speaking, CounselMate helps identify roles that align with your profile — including required skills, ideal education paths, average salary ranges, and growth opportunities.

This project is ideal for educational institutions, online career platforms, and individuals seeking self-assessment and direction. It’s scalable, easy to use, and designed to evolve with user needs.



 💻 Tech Stack

| Layer     | Technologies Used                        |
|-----------|------------------------------------------|
| AI Model  | Mistral-7B (for NLP career recommendations) |
| Backend   | Python (Flask), MongoDB                  |
| Frontend  | React.js (with Axios)                    |
| Database  | MongoDB                                  |

 🚀 How to Run the Project Locally
 ⚙️ 1. Backend Setup

Open your terminal and follow these steps:


# Step into the backend directory
cd chat/backend

# Install required Python dependencies
pip install -r requirements.txt

# Create an initial admin user
python admin_creation.py

# Seed the career-related data into the database
python data_seeder.py

# Start the backend server
python app.py

# Open a new terminal window
# Step into the frontend directory
cd chat/counselmate-frontend

# Start the React development server
npm start
