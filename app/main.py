from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Database importları - get_db'yi EKLE!
from app.database import engine, Base, get_db
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
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Şifreleme yapma, direkt kaydet
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(user: schemas.UserCreate):
    # HER ZAMAN AYNI TOKEN'I DÖNDÜR
    return {"access_token": "test-token-123", "token_type": "bearer"}

@app.post("/notes", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_note = Note(
        raw_text=note.raw_text,
        user_id=current_user["id"],  # dict olduğu için ["id"] kullan
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
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Note).filter(Note.id == note_id)
    if current_user["role"] != UserRole.ADMIN:
        query = query.filter(Note.user_id == current_user["id"])
    
    db_note = query.first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return db_note

@app.get("/notes", response_model=List[schemas.Note])
def get_notes(
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Note)
    if current_user["role"] != UserRole.ADMIN:
        query = query.filter(Note.user_id == current_user["id"])
    
    return query.all()

@app.get("/")
def read_root():
    return {"message": "Notes API is running!"}