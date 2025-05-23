from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.models.event import EventStatus

class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int = Field(default=0, ge=0)
    price: float = Field(default=0.0, ge=0)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    capacity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)
    status: Optional[EventStatus] = None

class EventResponse(EventBase):
    id: int
    status: EventStatus
    organizer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    attendee_count: int = 0
    available_seats: int = 0

    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    events: List[EventResponse]
    total: int
    skip: int
    limit: int