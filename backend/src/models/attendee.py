from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.core.database import Base

class AttendeeStatus(str, enum.Enum):
    REGISTERED = "registered"
    CHECKED_IN = "checked_in"
    CANCELLED = "cancelled"

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(AttendeeStatus), default=AttendeeStatus.REGISTERED)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    check_in_date = Column(DateTime(timezone=True), nullable=True)
    ticket_number = Column(String(100), unique=True, index=True)
    
    event = relationship("Event", back_populates="attendees")
    user = relationship("User", backref="attended_events")