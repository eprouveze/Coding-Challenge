from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db
from ..tasks import process_waitlist

router = APIRouter(prefix="/attendees", tags=["attendees"])

@router.post("/register", response_model=schemas.AttendeeRegistration)
async def register_for_event(
    registration: schemas.AttendeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    existing_registration = db.query(models.Attendee).filter(
        models.Attendee.event_id == registration.event_id,
        models.Attendee.user_id == current_user.id
    ).first()
    
    if existing_registration:
        if existing_registration.status == models.AttendanceStatus.CANCELLED:
            existing_registration.status = models.AttendanceStatus.REGISTERED
            existing_registration.registered_at = datetime.utcnow()
            db.commit()
            return schemas.AttendeeRegistration(
                message="Re-registered for event successfully",
                status=models.AttendanceStatus.REGISTERED
            )
        else:
            raise HTTPException(status_code=400, detail="Already registered for this event")
    
    current_attendees = db.query(func.count(models.Attendee.id)).filter(
        models.Attendee.event_id == registration.event_id,
        models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
    ).scalar()
    
    if current_attendees >= event.capacity:
        waitlist_count = db.query(func.count(models.Attendee.id)).filter(
            models.Attendee.event_id == registration.event_id,
            models.Attendee.status == models.AttendanceStatus.WAITLISTED
        ).scalar()
        
        new_attendee = models.Attendee(
            event_id=registration.event_id,
            user_id=current_user.id,
            status=models.AttendanceStatus.WAITLISTED,
            waitlist_position=waitlist_count + 1
        )
        db.add(new_attendee)
        db.commit()
        
        return schemas.AttendeeRegistration(
            message="Event is full. Added to waitlist",
            status=models.AttendanceStatus.WAITLISTED,
            waitlist_position=waitlist_count + 1
        )
    
    new_attendee = models.Attendee(
        event_id=registration.event_id,
        user_id=current_user.id,
        status=models.AttendanceStatus.REGISTERED
    )
    db.add(new_attendee)
    db.commit()
    
    return schemas.AttendeeRegistration(
        message="Registered for event successfully",
        status=models.AttendanceStatus.REGISTERED
    )

@router.put("/{attendee_id}/check-in", response_model=schemas.Attendee)
async def check_in_attendee(
    attendee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    attendee = db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee registration not found")
    
    if attendee.status != models.AttendanceStatus.REGISTERED:
        raise HTTPException(status_code=400, detail="Attendee must be registered to check in")
    
    attendee.status = models.AttendanceStatus.CHECKED_IN
    attendee.checked_in_at = datetime.utcnow()
    db.commit()
    db.refresh(attendee)
    
    return attendee

@router.put("/{attendee_id}/cancel", response_model=schemas.Attendee)
async def cancel_registration(
    attendee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    attendee = db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee registration not found")
    
    if attendee.user_id != current_user.id and current_user.role not in [models.UserRole.ADMIN, models.UserRole.ORGANIZER]:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this registration")
    
    if attendee.status == models.AttendanceStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Registration already cancelled")
    
    attendee.status = models.AttendanceStatus.CANCELLED
    db.commit()
    
    if attendee.status == models.AttendanceStatus.WAITLISTED:
        waitlisted_attendees = db.query(models.Attendee).filter(
            models.Attendee.event_id == attendee.event_id,
            models.Attendee.status == models.AttendanceStatus.WAITLISTED,
            models.Attendee.waitlist_position > attendee.waitlist_position
        ).all()
        
        for wa in waitlisted_attendees:
            wa.waitlist_position -= 1
        db.commit()
    else:
        process_waitlist.delay(attendee.event_id)
    
    db.refresh(attendee)
    return attendee

@router.get("/my-registrations", response_model=List[schemas.Attendee])
async def get_my_registrations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    registrations = db.query(models.Attendee).filter(
        models.Attendee.user_id == current_user.id
    ).all()
    return registrations

@router.get("/event/{event_id}", response_model=List[schemas.Attendee])
async def get_event_attendees(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user.role == models.UserRole.ORGANIZER and event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view attendees for this event")
    
    attendees = db.query(models.Attendee).filter(
        models.Attendee.event_id == event_id
    ).order_by(models.Attendee.registered_at).all()
    
    return attendees