# Notes API

A production-style REST API built with FastAPI, featuring JWT authentication, PostgreSQL, and a fully automated CI/CD pipeline.

🔗 **Live API:** https://notes-api-5cfd.onrender.com/docs

## Features

- User signup and login with JWT tokens
- Password hashing with bcrypt
- Full CRUD for notes (create, read, update, delete)
- Comments on notes, scoped to the note's owner
- Users can only access their own notes
- Automated testing with pytest
- CI/CD pipeline with GitHub Actions (auto-test + auto-deploy)
- Containerized with Docker

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (hosted on Neon)
- **ORM:** SQLAlchemy
- **Auth:** JWT (python-jose) + bcrypt password hashing
- **Testing:** pytest + TestClient
- **CI/CD:** GitHub Actions
- **Deployment:** Docker + Render

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|--------------|----------------|
| POST | `/signup` | Register a new user | No |
| POST | `/login` | Login, returns JWT token | No |
| POST | `/notes` | Create a new note | Yes |
| GET | `/notes` | Get all notes for current user | Yes |
| GET | `/notes/{id}` | Get a specific note | Yes |
| PUT | `/notes/{id}` | Update a note | Yes |
| DELETE | `/notes/{id}` | Delete a note | Yes |
| POST | `/notes/{id}/comments` | Add a comment to a note | Yes |
| GET | `/notes/{id}/comments` | Get comments on a note | Yes |

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Running with Docker Compose

```bash
docker-compose up --build
```

## Running Tests

```bash
pytest test_main.py -v
```

## Environment Variables

See `.env.example` for required variables. Copy it to `.env` and fill in your own values:

```bash
cp .env.example .env
```