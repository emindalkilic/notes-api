from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Sadece gereken importlar
from app.database import engine, Base, get_db
from app.models import User, Note, UserRole, NoteStatus
from app import schemas
from app.celery_worker import summarize_note_task

# Database tablolarını oluştur
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tabloları oluşturuldu!")
except Exception as e:
    print(f"❌ Database hatası: {e}")

app = FastAPI(title="Notes API", version="1.0.0")

# BASIT AUTH FUNCTIONS - auth.py'den kopyala
def get_current_user_simple():
    return {"id": 1, "email": "test@example.com", "role": "AGENT"}

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = next(get_db())):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(user: schemas.UserCreate):
    return {"access_token": "test-token-123", "token_type": "bearer"}

@app.post("/notes", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = next(get_db())):
    current_user = get_current_user_simple()
    
    db_note = Note(
        raw_text=note.raw_text,
        user_id=current_user["id"],
        status=NoteStatus.QUEUED
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    summarize_note_task.delay(db_note.id)
    return db_note

@app.get("/notes", response_model=List[schemas.Note])
def get_notes(db: Session = next(get_db())):
    current_user = get_current_user_simple()
    
    query = db.query(Note)
    if current_user["role"] != UserRole.ADMIN:
        query = query.filter(Note.user_id == current_user["id"])
    
    return query.all()

@app.get("/")
def read_root():
    return {"message": "Notes API is running!"}