# DQMS (Doctor Queue Management System)

DQMS is a full-stack web application designed to streamline patient queue management in hospitals. It allows patients to book tokens, view time slots, and hospitals to manage queues efficiently.

## Features

- User authentication for patients and hospitals
- Token booking system for patients
- Hospital management dashboard
- RESTful API backend with Flask and PostgreSQL
- Frontend built with Vue.js and Axios for API calls
- CORS handling for local development


## Prerequisites

Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.4
Flask-CORS==4.0.2
python-dotenv==1.0.0
psycopg2-binary
PyJWT==2.7.0


## Tech Stack

- Backend: Flask, SQLAlchemy, PostgreSQL
- Frontend: Vue.js
- Database: Flask-CORS, Supabase 


## Backend Setup (Flask)

1. Navigate to backend folder:
   cd backend

2. Create and activate virtual environment:
   python -m venv venv
   venv\Scripts\activate         

3. Install Python dependencies:
   pip install -r requirements.txt

4. Configure environment variables:

   Create a .env file or set environment variables:

   DATABASE_URL=postgresql://username:password@host:port/database
   SECRET_KEY=your_secret_key_here

5. Run database migrations:
   flask db upgrade

6. Run the Flask app:
   python run.py


## Frontend Setup (Vue.js)

1. Navigate to frontend folder:
   cd frontend

2. Install dependencies:
   npm install

3. Run development server:
   npm run dev

4. The frontend will be available at:
   http://localhost:5173