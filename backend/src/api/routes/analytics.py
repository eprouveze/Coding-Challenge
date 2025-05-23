from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional

from src.core.database import get_db
from src.services.auth import AuthService
from src.services.analytics import AnalyticsService
from src.schemas.analytics import EventAnalytics, DashboardAnalytics
from src.models.user import User

router = APIRouter()

@router.get("/dashboard", response_model=DashboardAnalytics)
async def get_dashboard_analytics(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(AuthService.get_current_admin_user),
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_dashboard_analytics(start_date, end_date)

@router.get("/events/{event_id}", response_model=EventAnalytics)
async def get_event_analytics(
    event_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    
    # Verify user has access to this event's analytics
    from src.services.event import EventService
    event_service = EventService(db)
    event = event_service.get_event(event_id)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.organizer_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view analytics for this event"
        )
    
    return analytics_service.get_event_analytics(event_id)

@router.get("/revenue")
async def get_revenue_analytics(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    group_by: str = Query("month", regex="^(day|week|month|year)$"),
    current_user: User = Depends(AuthService.get_current_admin_user),
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_revenue_analytics(start_date, end_date, group_by)

@router.get("/attendance-trends")
async def get_attendance_trends(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    event_id: Optional[int] = None,
    current_user: User = Depends(AuthService.get_current_admin_user),
    db: Session = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_attendance_trends(start_date, end_date, event_id)