from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

app = FastAPI()

SECRET_KEY = "my-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

fake_users_db = {}
fake_notes_db = {}
note_id_counter = 1

class UserSignup(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=4, max_length=50)

class Note(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

@app.post("/signup")
def signup(user: UserSignup):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": pwd_context.hash(user.password)
    }
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes")
def create_note(note: Note, current_user: str = Depends(get_current_user)):
    global note_id_counter
    note_id = note_id_counter
    fake_notes_db[note_id] = {
        "id": note_id,
        "title": note.title,
        "content": note.content,
        "owner": current_user
    }
    note_id_counter += 1
    return {"message": "Note created", "note": fake_notes_db[note_id]}

@app.get("/notes")
def get_my_notes(current_user: str = Depends(get_current_user)):
    my_notes = [n for n in fake_notes_db.values() if n["owner"] == current_user]
    return {"notes": my_notes}

@app.get("/notes/{note_id}")
def get_note(note_id: int, current_user: str = Depends(get_current_user)):
    note = fake_notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["owner"] != current_user:
        raise HTTPException(status_code=403, detail="You don't own this note")
    return note

@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note, current_user: str = Depends(get_current_user)):
    note = fake_notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["owner"] != current_user:
        raise HTTPException(status_code=403, detail="You don't own this note")
    note["title"] = updated_note.title
    note["content"] = updated_note.content
    return {"message": "Note updated", "note": note}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, current_user: str = Depends(get_current_user)):
    note = fake_notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["owner"] != current_user:
        raise HTTPException(status_code=403, detail="You don't own this note")
    del fake_notes_db[note_id]
    return {"message": "Note deleted"}

@app.get("/")
def read_root():
    return {"message": "Notes API is running!"}