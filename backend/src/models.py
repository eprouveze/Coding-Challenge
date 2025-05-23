from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class EventCategory(str, enum.Enum):
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    NETWORKING = "networking"
    SOCIAL = "social"
    TRAINING = "training"
    OTHER = "other"

class AttendanceStatus(str, enum.Enum):
    REGISTERED = "registered"
    CHECKED_IN = "checked_in"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    ATTENDEE = "attendee"

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    location = Column(String(300), nullable=False)
    capacity = Column(Integer, nullable=False)
    category = Column(Enum(EventCategory), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    attendees = relationship("Attendee", back_populates="event", cascade="all, delete-orphan")
    organizer_id = Column(Integer, ForeignKey("users.id"))
    organizer = relationship("User", back_populates="organized_events")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.ATTENDEE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organized_events = relationship("Event", back_populates="organizer")
    attendances = relationship("Attendee", back_populates="user")

class Attendee(Base):
    __tablename__ = "attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.REGISTERED)
    registered_at = Column(DateTime, default=datetime.utcnow)
    checked_in_at = Column(DateTime, nullable=True)
    waitlist_position = Column(Integer, nullable=True)
    
    event = relationship("Event", back_populates="attendees")
    user = relationship("User", back_populates="attendances")
    
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )