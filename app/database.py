from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Render'ın otomatik verdiği DATABASE_URL'i kullan
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Eğer DATABASE_URL yoksa (local development için)
    DATABASE_URL = "postgresql://user:password@localhost:5432/notesdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()