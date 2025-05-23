from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Tuple, Optional
from datetime import datetime
import uuid

from src.models.event import Event, EventStatus
from src.models.attendee import Attendee, AttendeeStatus
from src.schemas.event import EventCreate, EventUpdate
from fastapi import HTTPException, status

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event_data: EventCreate, organizer_id: int) -> Event:
        db_event = Event(
            **event_data.dict(),
            organizer_id=organizer_id,
            status=EventStatus.DRAFT
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_event(self, event_id: int) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def list_events(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Event], int]:
        query = self.db.query(Event)
        
        if status:
            query = query.filter(Event.status == status)
        
        if search:
            search_filter = or_(
                Event.title.ilike(f"%{search}%"),
                Event.description.ilike(f"%{search}%"),
                Event.location.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        total = query.count()
        events = query.offset(skip).limit(limit).all()
        
        # Add attendee count to each event
        for event in events:
            event.attendee_count = self.db.query(Attendee).filter(
                Attendee.event_id == event.id,
                Attendee.status != AttendeeStatus.CANCELLED
            ).count()
            event.available_seats = max(0, event.capacity - event.attendee_count)
        
        return events, total

    def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        event = self.get_event(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        update_data = event_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)
        
        self.db.commit()
        self.db.refresh(event)
        return event

    def delete_event(self, event_id: int):
        event = self.get_event(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        self.db.delete(event)
        self.db.commit()

    def register_attendee(self, event_id: int, user_id: int) -> Attendee:
        event = self.get_event(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        # Check if user is already registered
        existing = self.db.query(Attendee).filter(
            Attendee.event_id == event_id,
            Attendee.user_id == user_id,
            Attendee.status != AttendeeStatus.CANCELLED
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already registered for this event"
            )
        
        # Check capacity
        current_attendees = self.db.query(Attendee).filter(
            Attendee.event_id == event_id,
            Attendee.status != AttendeeStatus.CANCELLED
        ).count()
        
        if event.capacity > 0 and current_attendees >= event.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is full"
            )
        
        # Create attendee record
        attendee = Attendee(
            event_id=event_id,
            user_id=user_id,
            ticket_number=f"TKT-{uuid.uuid4().hex[:8].upper()}"
        )
        self.db.add(attendee)
        self.db.commit()
        self.db.refresh(attendee)
        
        return attendee