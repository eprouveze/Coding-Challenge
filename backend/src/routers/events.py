from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    db_event = models.Event(**event.dict(), organizer_id=current_user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    db_event.current_attendees = 0
    db_event.available_spots = db_event.capacity
    
    return db_event

@router.get("/", response_model=List[schemas.Event])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[models.EventCategory] = None,
    upcoming_only: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(models.Event)
    
    if category:
        query = query.filter(models.Event.category == category)
    
    if upcoming_only:
        query = query.filter(models.Event.date >= datetime.utcnow())
    
    events = query.offset(skip).limit(limit).all()
    
    for event in events:
        attendee_count = db.query(func.count(models.Attendee.id)).filter(
            models.Attendee.event_id == event.id,
            models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
        ).scalar()
        
        event.current_attendees = attendee_count
        event.available_spots = max(0, event.capacity - attendee_count)
    
    return events

@router.get("/{event_id}", response_model=schemas.EventWithAttendees)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    attendee_count = db.query(func.count(models.Attendee.id)).filter(
        models.Attendee.event_id == event.id,
        models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
    ).scalar()
    
    event.current_attendees = attendee_count
    event.available_spots = max(0, event.capacity - attendee_count)
    
    return event

@router.put("/{event_id}", response_model=schemas.Event)
async def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user.role == models.UserRole.ORGANIZER and event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(event)
    
    attendee_count = db.query(func.count(models.Attendee.id)).filter(
        models.Attendee.event_id == event.id,
        models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
    ).scalar()
    
    event.current_attendees = attendee_count
    event.available_spots = max(0, event.capacity - attendee_count)
    
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user.role == models.UserRole.ORGANIZER and event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    db.delete(event)
    db.commit()
    return None