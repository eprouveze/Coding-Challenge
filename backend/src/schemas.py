from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from .models import EventCategory, AttendanceStatus, UserRole

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    date: datetime
    location: str = Field(..., min_length=1, max_length=300)
    capacity: int = Field(..., gt=0)
    category: EventCategory

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    capacity: Optional[int] = Field(None, gt=0)
    category: Optional[EventCategory] = None

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    organizer_id: int
    organizer: User
    current_attendees: int = 0
    available_spots: int = 0
    
    class Config:
        from_attributes = True

class AttendeeBase(BaseModel):
    event_id: int
    user_id: int

class AttendeeCreate(BaseModel):
    event_id: int

class AttendeeUpdate(BaseModel):
    status: AttendanceStatus

class Attendee(AttendeeBase):
    id: int
    status: AttendanceStatus
    registered_at: datetime
    checked_in_at: Optional[datetime] = None
    waitlist_position: Optional[int] = None
    user: User
    
    class Config:
        from_attributes = True

class EventWithAttendees(Event):
    attendees: List[Attendee] = []

class EventStatistics(BaseModel):
    total_events: int
    total_attendees: int
    average_attendance_rate: float
    events_by_category: dict
    upcoming_events: int
    past_events: int
    most_popular_category: str
    events_at_capacity: int

class UserStatistics(BaseModel):
    total_users: int
    users_by_role: dict
    active_users: int
    new_users_this_month: int

class AttendeeRegistration(BaseModel):
    message: str
    status: AttendanceStatus
    waitlist_position: Optional[int] = None