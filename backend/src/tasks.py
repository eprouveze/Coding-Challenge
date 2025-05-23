from celery import Celery
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from .config import settings
from .database import SessionLocal
from . import models

celery_app = Celery("event_management", broker=settings.redis_url)

@celery_app.task
def process_waitlist(event_id: int):
    db = SessionLocal()
    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            return
        
        current_attendees = db.query(func.count(models.Attendee.id)).filter(
            models.Attendee.event_id == event_id,
            models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
        ).scalar()
        
        available_spots = event.capacity - current_attendees
        
        if available_spots > 0:
            waitlisted_attendees = db.query(models.Attendee).filter(
                models.Attendee.event_id == event_id,
                models.Attendee.status == models.AttendanceStatus.WAITLISTED
            ).order_by(models.Attendee.waitlist_position).limit(available_spots).all()
            
            for attendee in waitlisted_attendees:
                attendee.status = models.AttendanceStatus.REGISTERED
                attendee.waitlist_position = None
                attendee.registered_at = datetime.utcnow()
            
            remaining_waitlisted = db.query(models.Attendee).filter(
                models.Attendee.event_id == event_id,
                models.Attendee.status == models.AttendanceStatus.WAITLISTED
            ).order_by(models.Attendee.waitlist_position).all()
            
            for i, attendee in enumerate(remaining_waitlisted, 1):
                attendee.waitlist_position = i
            
            db.commit()
    finally:
        db.close()

@celery_app.task
def send_event_reminder(event_id: int):
    db = SessionLocal()
    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event:
            return
        
        attendees = db.query(models.Attendee).filter(
            models.Attendee.event_id == event_id,
            models.Attendee.status == models.AttendanceStatus.REGISTERED
        ).all()
        
        for attendee in attendees:
            print(f"Sending reminder to {attendee.user.email} for event {event.title}")
    finally:
        db.close()

@celery_app.task
def cleanup_past_events():
    db = SessionLocal()
    try:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        old_events = db.query(models.Event).filter(
            models.Event.date < thirty_days_ago
        ).all()
        
        for event in old_events:
            print(f"Archiving event: {event.title}")
    finally:
        db.close()