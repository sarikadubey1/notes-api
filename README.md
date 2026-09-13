# Notes API

A REST API built with FastAPI featuring JWT authentication.

## Features
- User signup and login with JWT tokens
- Password hashing with bcrypt
- Full CRUD for notes (create, read, update, delete)
- Users can only access their own notes

## How to Run
pip install -r requirements.txt
uvicorn main:app --reload

Visit http://127.0.0.1:8000/docs for interactive API documentation.
