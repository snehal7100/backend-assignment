# FastAPI Backend Assignment

This project is a backend application developed using FastAPI. It provides user authentication and task management functionalities. The system allows users to register, log in securely, and manage their tasks efficiently through RESTful APIs.

## Features

* User Registration and Login with JWT Authentication
* Create, View, Update, and Delete Tasks
* Move Tasks between different statuses
* Dashboard API for task insights
* Secure and structured RESTful API
* SQLite database integration
* API testing using Swagger UI and Postman

## Technologies Used

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* Uvicorn
* JWT Authentication
* Postman
* Swagger UI

## Project Structure

```
backend-assignment/
│── main.py          # Main FastAPI application
│── models.py        # Database models
│── schemas.py       # Pydantic schemas
│── database.py      # Database configuration
│── auth.py          # Authentication and JWT logic
│── requirements.txt # Project dependencies
│── test.db          # SQLite database
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/snehal7100/backend-assignment.git
cd backend-assignment
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, access the API documentation using:

* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint         | Description                          |
| ------ | ---------------- | ------------------------------------ |
| POST   | /register        | Register a new user                  |
| POST   | /login           | Authenticate user and generate token |
| GET    | /users           | Retrieve all users                   |
| POST   | /tasks           | Create a new task                    |
| GET    | /tasks           | Retrieve all tasks                   |
| PUT    | /tasks/{task_id} | Update a task                        |
| DELETE | /tasks/{task_id} | Delete a task                        |
| POST   | /move-task       | Move a task to a new status          |
| GET    | /dashboard       | View dashboard statistics            |

## Testing 

The APIs were tested using:

* Swagger UI
* Postman

## Author

**Snehal Pawar**
FastAPI Backend Assignment
