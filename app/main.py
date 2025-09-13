from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Database importları
from app.database import engine, Base
from app.models import User, Note, UserRole, NoteStatus
from app import schemas
from app import auth
from app.celery_worker import summarize_note_task

# Database tablolarını oluştur
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tabloları oluşturuldu!")
except Exception as e:
    print(f"❌ Database hatası: {e}")

app = FastAPI(title="Notes API", version="1.0.0")

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/notes", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    db_note = Note(
        raw_text=note.raw_text,
        user_id=current_user.id,
        status=NoteStatus.QUEUED
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    # Background task'i başlat
    summarize_note_task.delay(db_note.id)
    
    return db_note

@app.get("/notes/{note_id}", response_model=schemas.Note)
def get_note(
    note_id: int,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    query = db.query(Note).filter(Note.id == note_id)
    if current_user.role != UserRole.ADMIN:
        query = query.filter(Note.user_id == current_user.id)
    
    db_note = query.first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return db_note

@app.get("/notes", response_model=List[schemas.Note])
def get_notes(
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    query = db.query(Note)
    if current_user.role != UserRole.ADMIN:
        query = query.filter(Note.user_id == current_user.id)
    
    return query.all()

@app.get("/")
def read_root():
    return {"message": "Notes API is running!"}