from celery import Celery
from sqlalchemy.orm import Session
import time
import random

from app.database import SessionLocal
from app.models import Note, NoteStatus

celery_app = Celery('worker')
celery_app.conf.broker_url = 'redis://redis:6379/0'

@celery_app.task
def summarize_note_task(note_id: int):
    db = SessionLocal()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return
        
        note.status = NoteStatus.PROCESSING
        db.commit()
        
        time.sleep(random.randint(2, 5))
        
        words = note.raw_text.split()
        if len(words) > 10:
            summary = " ".join(words[:10]) + "..."
        else:
            summary = note.raw_text
        
        note.summary = summary
        note.status = NoteStatus.DONE
        db.commit()
        
    except Exception as e:
        if note:
            note.status = NoteStatus.FAILED
            db.commit()
        raise e
    finally:
        db.close()