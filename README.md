#Expense Management System

Expense Tracking System

A simple yet powerful Expense Tracking System that helps users manage, track, and analyze their expenses efficiently. Built with a MySQL database, FastAPI backend, and Streamlit frontend.

Features

Add, edit, and delete expenses

View expense summaries by date or category

Analytics dashboard with category breakdowns and percentages

User-friendly frontend built with Streamlit

RESTful backend API built with FastAPI

MySQL database for persistent storage

Tech Stack
Layer	Technology
Frontend	Streamlit
Backend	FastAPI
Database	MySQL
API Requests	requests Python library
Deployment	Local / Cloud (optional)
Installation
Prerequisites

Python 3.11+

MySQL Server installed and running

pip package manager

Clone the repository
git clone <your-repo-url>
cd expense-tracking-system

Create and activate virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Database Setup

Start MySQL server and create a database:

CREATE DATABASE expense_tracker;


Create expenses table:

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    expense_date DATE NOT NULL,
    description VARCHAR(255)
);


Update your backend config with MySQL credentials:

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "<your-password>"
DB_NAME = "expense_tracker"

Running the Application
Backend (FastAPI)
uvicorn server:app --reload


Server will run at: http://127.0.0.1:8000

API docs available at: http://127.0.0.1:8000/docs

Frontend (Streamlit)
streamlit run app.py


Streamlit app will open in your browser.

Connects to FastAPI backend to fetch and display data.

API Endpoints
Endpoint	Method	Description
/expenses	POST	Add a new expense
/expenses/{date}	GET	Get expenses for a specific date
/analytics	POST	Get analytics summary for a date range