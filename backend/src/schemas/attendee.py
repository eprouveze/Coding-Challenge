from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from src.models.attendee import AttendeeStatus

class AttendeeBase(BaseModel):
    event_id: int
    user_id: int
    status: AttendeeStatus = AttendeeStatus.REGISTERED

class AttendeeCreate(AttendeeBase):
    pass

class AttendeeUpdate(BaseModel):
    status: Optional[AttendeeStatus] = None

class AttendeeResponse(AttendeeBase):
    id: int
    registration_date: datetime
    check_in_date: Optional[datetime] = None
    ticket_number: str

    class Config:
        from_attributes = True

class AttendeeListResponse(BaseModel):
    attendees: List[AttendeeResponse]
    total: int
    skip: int
    limit: int