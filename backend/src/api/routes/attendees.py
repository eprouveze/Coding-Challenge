from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.core.database import get_db
from src.services.auth import AuthService
from src.services.attendee import AttendeeService
from src.schemas.attendee import AttendeeResponse, AttendeeUpdate, AttendeeListResponse
from src.models.user import User

router = APIRouter()

@router.get("/", response_model=AttendeeListResponse)
async def list_attendees(
    event_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(AuthService.get_current_admin_user),
    db: Session = Depends(get_db)
):
    attendee_service = AttendeeService(db)
    attendees, total = attendee_service.list_attendees(
        event_id=event_id,
        user_id=user_id,
        status=status,
        skip=skip,
        limit=limit
    )
    return AttendeeListResponse(
        attendees=attendees,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{attendee_id}", response_model=AttendeeResponse)
async def get_attendee(
    attendee_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    attendee_service = AttendeeService(db)
    attendee = attendee_service.get_attendee(attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee record not found"
        )
    
    # Check if user can access this attendee record
    if (attendee.user_id != current_user.id and 
        not current_user.is_superuser and 
        attendee.event.organizer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this attendee record"
        )
    
    return attendee

@router.put("/{attendee_id}", response_model=AttendeeResponse)
async def update_attendee(
    attendee_id: int,
    attendee_data: AttendeeUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    attendee_service = AttendeeService(db)
    attendee = attendee_service.get_attendee(attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee record not found"
        )
    
    # Check authorization
    if (not current_user.is_superuser and 
        attendee.event.organizer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this attendee record"
        )
    
    updated_attendee = attendee_service.update_attendee(attendee_id, attendee_data)
    return updated_attendee

@router.post("/{attendee_id}/check-in", response_model=AttendeeResponse)
async def check_in_attendee(
    attendee_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    attendee_service = AttendeeService(db)
    attendee = attendee_service.get_attendee(attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee record not found"
        )
    
    # Check authorization
    if (not current_user.is_superuser and 
        attendee.event.organizer_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to check in this attendee"
        )
    
    checked_in_attendee = attendee_service.check_in_attendee(attendee_id)
    return checked_in_attendee