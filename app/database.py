from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Render otomatik olarak DATABASE_URL environment variable'ını ekliyor
DATABASE_URL = os.getenv("DATABASE_URL")

# Eğer DATABASE_URL yoksa local development için fallback
if not DATABASE_URL:
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