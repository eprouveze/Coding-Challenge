from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from .db import Base

class AttendanceStatus(str, enum.Enum):
    registered = "registered"
    checked_in = "checked_in"
    cancelled = "cancelled"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    date = Column(DateTime)
    location = Column(String)
    capacity = Column(Integer)
    category = Column(String, index=True)

    attendees = relationship("Attendee", back_populates="event")

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String)
    email = Column(String, index=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.registered)

    event = relationship("Event", back_populates="attendees")
