from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date

class EventAnalytics(BaseModel):
    event_id: int
    total_registrations: int
    total_check_ins: int
    check_in_rate: float
    revenue: float
    capacity_utilization: float
    registration_trend: List[Dict[str, Any]]

class DashboardAnalytics(BaseModel):
    total_events: int
    total_attendees: int
    total_revenue: float
    average_attendance_rate: float
    upcoming_events: int
    events_by_status: Dict[str, int]
    top_events: List[Dict[str, Any]]
    recent_registrations: List[Dict[str, Any]]