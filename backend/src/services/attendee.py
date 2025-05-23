from sqlalchemy.orm import Session
from typing import List, Tuple, Optional
from datetime import datetime

from src.models.attendee import Attendee, AttendeeStatus
from src.schemas.attendee import AttendeeUpdate
from fastapi import HTTPException, status

class AttendeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_attendee(self, attendee_id: int) -> Optional[Attendee]:
        return self.db.query(Attendee).filter(Attendee.id == attendee_id).first()

    def list_attendees(
        self,
        event_id: Optional[int] = None,
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Attendee], int]:
        query = self.db.query(Attendee)
        
        if event_id:
            query = query.filter(Attendee.event_id == event_id)
        
        if user_id:
            query = query.filter(Attendee.user_id == user_id)
        
        if status:
            query = query.filter(Attendee.status == status)
        
        total = query.count()
        attendees = query.offset(skip).limit(limit).all()
        
        return attendees, total

    def update_attendee(self, attendee_id: int, attendee_data: AttendeeUpdate) -> Attendee:
        attendee = self.get_attendee(attendee_id)
        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendee record not found"
            )
        
        update_data = attendee_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(attendee, field, value)
        
        self.db.commit()
        self.db.refresh(attendee)
        return attendee

    def check_in_attendee(self, attendee_id: int) -> Attendee:
        attendee = self.get_attendee(attendee_id)
        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendee record not found"
            )
        
        if attendee.status == AttendeeStatus.CHECKED_IN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendee already checked in"
            )
        
        if attendee.status == AttendeeStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot check in cancelled registration"
            )
        
        attendee.status = AttendeeStatus.CHECKED_IN
        attendee.check_in_date = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(attendee)
        return attendee

    def cancel_registration(self, attendee_id: int) -> Attendee:
        attendee = self.get_attendee(attendee_id)
        if not attendee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendee record not found"
            )
        
        if attendee.status == AttendeeStatus.CHECKED_IN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel after check-in"
            )
        
        attendee.status = AttendeeStatus.CANCELLED
        
        self.db.commit()
        self.db.refresh(attendee)
        return attendee