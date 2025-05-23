from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/events", response_model=schemas.EventStatistics)
async def get_event_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    total_events = db.query(func.count(models.Event.id)).scalar()
    
    total_attendees = db.query(func.count(models.Attendee.id)).filter(
        models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
    ).scalar()
    
    events_with_capacity = db.query(
        models.Event.id,
        models.Event.capacity,
        func.count(models.Attendee.id).label('attendee_count')
    ).outerjoin(
        models.Attendee,
        and_(
            models.Event.id == models.Attendee.event_id,
            models.Attendee.status.in_([models.AttendanceStatus.REGISTERED, models.AttendanceStatus.CHECKED_IN])
        )
    ).group_by(models.Event.id, models.Event.capacity).all()
    
    total_capacity = sum(event.capacity for event in events_with_capacity)
    total_attendance = sum(event.attendee_count for event in events_with_capacity)
    average_attendance_rate = (total_attendance / total_capacity * 100) if total_capacity > 0 else 0
    
    events_at_capacity = sum(1 for event in events_with_capacity if event.attendee_count >= event.capacity)
    
    events_by_category = db.query(
        models.Event.category,
        func.count(models.Event.id)
    ).group_by(models.Event.category).all()
    
    category_dict = {str(category): count for category, count in events_by_category}
    
    upcoming_events = db.query(func.count(models.Event.id)).filter(
        models.Event.date >= datetime.utcnow()
    ).scalar()
    
    past_events = total_events - upcoming_events
    
    most_popular_category = max(category_dict.items(), key=lambda x: x[1])[0] if category_dict else "None"
    
    return schemas.EventStatistics(
        total_events=total_events,
        total_attendees=total_attendees,
        average_attendance_rate=round(average_attendance_rate, 2),
        events_by_category=category_dict,
        upcoming_events=upcoming_events,
        past_events=past_events,
        most_popular_category=most_popular_category,
        events_at_capacity=events_at_capacity
    )

@router.get("/users", response_model=schemas.UserStatistics)
async def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN]))
):
    total_users = db.query(func.count(models.User.id)).scalar()
    
    users_by_role = db.query(
        models.User.role,
        func.count(models.User.id)
    ).group_by(models.User.role).all()
    
    role_dict = {str(role): count for role, count in users_by_role}
    
    active_users = db.query(func.count(models.User.id)).filter(
        models.User.is_active == True
    ).scalar()
    
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    new_users_this_month = db.query(func.count(models.User.id)).filter(
        models.User.created_at >= one_month_ago
    ).scalar()
    
    return schemas.UserStatistics(
        total_users=total_users,
        users_by_role=role_dict,
        active_users=active_users,
        new_users_this_month=new_users_this_month
    )

@router.get("/events/{event_id}/stats")
async def get_event_specific_statistics(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.ORGANIZER]))
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user.role == models.UserRole.ORGANIZER and event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view statistics for this event")
    
    attendee_stats = db.query(
        models.Attendee.status,
        func.count(models.Attendee.id)
    ).filter(
        models.Attendee.event_id == event_id
    ).group_by(models.Attendee.status).all()
    
    status_dict = {str(status): count for status, count in attendee_stats}
    
    checked_in_count = status_dict.get(str(models.AttendanceStatus.CHECKED_IN), 0)
    registered_count = status_dict.get(str(models.AttendanceStatus.REGISTERED), 0)
    total_confirmed = checked_in_count + registered_count
    
    attendance_rate = (total_confirmed / event.capacity * 100) if event.capacity > 0 else 0
    check_in_rate = (checked_in_count / total_confirmed * 100) if total_confirmed > 0 else 0
    
    return {
        "event_id": event_id,
        "event_title": event.title,
        "capacity": event.capacity,
        "attendee_breakdown": status_dict,
        "total_confirmed": total_confirmed,
        "attendance_rate": round(attendance_rate, 2),
        "check_in_rate": round(check_in_rate, 2),
        "available_spots": max(0, event.capacity - total_confirmed),
        "is_full": total_confirmed >= event.capacity
    }