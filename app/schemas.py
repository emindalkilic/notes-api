from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    raw_text: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    summary: Optional[str] = None
    status: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True