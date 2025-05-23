from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .models import AttendanceStatus

class AttendeeBase(BaseModel):
    name: str
    email: str

class AttendeeCreate(AttendeeBase):
    pass

class Attendee(AttendeeBase):
    id: int
    status: AttendanceStatus

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: str
    capacity: int
    category: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    attendees: List[Attendee] = []

    class Config:
        orm_mode = True
