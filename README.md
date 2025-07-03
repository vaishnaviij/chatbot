# CounselMate - Your Career Counseling Companion

CounselMate is an AI-powered career guidance platform designed to help students explore and discover suitable career paths based on their unique skills, interests, and educational backgrounds.

> Developed as a major college project by  
> Nandini Goyal, Rishika Raj, and Vaishnavi Jadon

---

## Key Components Explained

### 1. Chatbot Core Features

- Natural Language Processing (NLP)  
  Uses Hugging Face’s Zephyr-7B-beta model for generating responses.  
  Extracts career interests and skills from user input using regex patterns.

- Personalization  
  Stores user preferences (skills, interests, education background) in MongoDB.  
  Dynamically recommends careers tailored to individual users.

- Conversation Flow  
  Follows a structured SYSTEM_PROMPT to simulate a professional career counselor.  
  Maintains conversational context with a 5-message history window.


## Prerequisites

Before running the project locally, make sure you have the following installed:

- Python 3.7+  
- Node.js (v14+ recommended)  
- pip (Python package manager)
Here’s your content restructured with clear spacing between steps and sections for improved readability:

---

## 1. Clone the Repository

```bash
git clone https://github.com/rishika2108/counselmate.git
cd counselmate
```

---

## 2. Configure MongoDB

* Log in to [MongoDB Atlas](https://cloud.mongodb.com/)
* Create a new cluster
* Select Python as the driver
* Copy the connection URI and paste it inside:

```python
backend/config.py:

MONGO_URI = "your-mongo-uri"
```

---

## 3. Configure Hugging Face API

* Log in at [huggingface.co](https://huggingface.co/)
* Go to Settings → Access Tokens
* Generate a new token
* Paste the token in:

```python
backend/config.py:

HF_TOKEN = "your-token"
```

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python admin_creation.py
python data_seeder.py
python app.py
```

---

## Frontend Setup

In a new terminal:

```bash
cd counselmate-frontend
npm install
npm start
```

Then visit:
[http://localhost:3000](http://localhost:3000) to start using CounselMate!

---

## Team Credits

Built with passion by:

* Nandini Goyal
* Rishika Raj
* Vaishnavi Jadon

---

## License

This project is developed for educational and demonstration purposes only.
It may be freely modified or extended for personal, academic, or non-commercial use.
Commercial use requires permission from the authors.











