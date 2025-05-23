from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .db import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events/", response_model=List[schemas.Event])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Event).offset(skip).limit(limit).all()

@app.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/events/{event_id}/register", response_model=schemas.Attendee)
def register_attendee(event_id: int, attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if len(event.attendees) >= event.capacity:
        raise HTTPException(status_code=400, detail="Event full")
    db_attendee = models.Attendee(event_id=event_id, **attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

@app.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    total_events = db.query(models.Event).count()
    total_attendees = db.query(models.Attendee).count()
    return {"total_events": total_events, "total_attendees": total_attendees}
