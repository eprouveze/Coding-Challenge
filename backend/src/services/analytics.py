from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta

from src.models.event import Event, EventStatus
from src.models.attendee import Attendee, AttendeeStatus
from src.models.user import User
from src.schemas.analytics import EventAnalytics, DashboardAnalytics

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_event_analytics(self, event_id: int) -> EventAnalytics:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        
        total_registrations = self.db.query(Attendee).filter(
            Attendee.event_id == event_id,
            Attendee.status != AttendeeStatus.CANCELLED
        ).count()
        
        total_check_ins = self.db.query(Attendee).filter(
            Attendee.event_id == event_id,
            Attendee.status == AttendeeStatus.CHECKED_IN
        ).count()
        
        check_in_rate = (total_check_ins / total_registrations * 100) if total_registrations > 0 else 0
        revenue = total_registrations * event.price
        capacity_utilization = (total_registrations / event.capacity * 100) if event.capacity > 0 else 0
        
        # Get registration trend (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        registration_trend = self.db.query(
            func.date(Attendee.registration_date).label('date'),
            func.count(Attendee.id).label('count')
        ).filter(
            Attendee.event_id == event_id,
            Attendee.registration_date >= thirty_days_ago
        ).group_by(func.date(Attendee.registration_date)).all()
        
        trend_data = [{"date": str(item.date), "count": item.count} for item in registration_trend]
        
        return EventAnalytics(
            event_id=event_id,
            total_registrations=total_registrations,
            total_check_ins=total_check_ins,
            check_in_rate=check_in_rate,
            revenue=revenue,
            capacity_utilization=capacity_utilization,
            registration_trend=trend_data
        )

    def get_dashboard_analytics(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> DashboardAnalytics:
        query = self.db.query(Event)
        
        if start_date:
            query = query.filter(Event.start_date >= start_date)
        if end_date:
            query = query.filter(Event.end_date <= end_date)
        
        total_events = query.count()
        
        # Total attendees
        total_attendees = self.db.query(Attendee).filter(
            Attendee.status != AttendeeStatus.CANCELLED
        ).count()
        
        # Total revenue
        total_revenue = self.db.query(
            func.sum(Event.price * func.count(Attendee.id))
        ).join(Attendee).filter(
            Attendee.status != AttendeeStatus.CANCELLED
        ).scalar() or 0
        
        # Average attendance rate
        events_with_capacity = self.db.query(Event).filter(Event.capacity > 0).all()
        if events_with_capacity:
            total_rate = 0
            count = 0
            for event in events_with_capacity:
                attendees = self.db.query(Attendee).filter(
                    Attendee.event_id == event.id,
                    Attendee.status != AttendeeStatus.CANCELLED
                ).count()
                total_rate += (attendees / event.capacity)
                count += 1
            average_attendance_rate = (total_rate / count * 100) if count > 0 else 0
        else:
            average_attendance_rate = 0
        
        # Upcoming events
        upcoming_events = self.db.query(Event).filter(
            Event.start_date > datetime.utcnow(),
            Event.status == EventStatus.PUBLISHED
        ).count()
        
        # Events by status
        events_by_status = {}
        for status in EventStatus:
            count = self.db.query(Event).filter(Event.status == status).count()
            events_by_status[status.value] = count
        
        # Top events by attendees
        top_events_query = self.db.query(
            Event.id,
            Event.title,
            func.count(Attendee.id).label('attendee_count')
        ).join(Attendee).filter(
            Attendee.status != AttendeeStatus.CANCELLED
        ).group_by(Event.id).order_by(func.count(Attendee.id).desc()).limit(5).all()
        
        top_events = [
            {"id": event.id, "title": event.title, "attendee_count": event.attendee_count}
            for event in top_events_query
        ]
        
        # Recent registrations
        recent_registrations_query = self.db.query(
            Attendee.id,
            User.username,
            Event.title,
            Attendee.registration_date
        ).join(User).join(Event).order_by(
            Attendee.registration_date.desc()
        ).limit(10).all()
        
        recent_registrations = [
            {
                "id": reg.id,
                "username": reg.username,
                "event_title": reg.title,
                "registration_date": reg.registration_date.isoformat()
            }
            for reg in recent_registrations_query
        ]
        
        return DashboardAnalytics(
            total_events=total_events,
            total_attendees=total_attendees,
            total_revenue=total_revenue,
            average_attendance_rate=average_attendance_rate,
            upcoming_events=upcoming_events,
            events_by_status=events_by_status,
            top_events=top_events,
            recent_registrations=recent_registrations
        )

    def get_revenue_analytics(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        group_by: str = "month"
    ) -> List[Dict[str, Any]]:
        # Implementation would depend on the specific database and requirements
        # This is a placeholder that returns sample data
        return [
            {"period": "2024-01", "revenue": 15000},
            {"period": "2024-02", "revenue": 22000},
            {"period": "2024-03", "revenue": 18500}
        ]

    def get_attendance_trends(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        event_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        # Implementation would show attendance trends over time
        # This is a placeholder that returns sample data
        return [
            {"date": "2024-01-15", "registrations": 45, "check_ins": 40},
            {"date": "2024-01-16", "registrations": 52, "check_ins": 48},
            {"date": "2024-01-17", "registrations": 38, "check_ins": 35}
        ]